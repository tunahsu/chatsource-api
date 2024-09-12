import uuid
import google.generativeai as genai

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.schemas.chatbots import ChatbotCreate, ChatbotResponse, ChatbotQuery
from app.models import User, Chatbot, UserRole, UserChatbot
from app.core.db import get_async_session
from app.core.users import current_active_user
from app.core.exception import NewHTTPException
from app.core.config import settings

chatbot_router = APIRouter(prefix='/chatbots', tags=['Chatbots'])


@chatbot_router.get('/list', response_model=list[dict])
async def get_chatbot_list(user: User = Depends(current_active_user),
                           session: AsyncSession = Depends(get_async_session)):
    chatbots_list = []
    chatbots = (await session.execute(
        select(Chatbot).join(UserChatbot).filter(
            UserChatbot.user_id == user.id))).scalars().all()
    for chatbot in chatbots:
        user_chatbots = (await session.execute(
            select(UserChatbot).join(User).filter(
                UserChatbot.chatbot_id == chatbot.id))).scalars().all()
        chatbot_dict = ChatbotResponse.model_validate(chatbot).model_dump()
        chatbot_dict.update({
            'members': [{
                'id': user_chatbot.user.id,
                'email': user_chatbot.user.email,
                'role': user_chatbot.role
            } for user_chatbot in user_chatbots]
        })
        chatbots_list.append(chatbot_dict)
    return chatbots_list


@chatbot_router.post('/create',
                     status_code=201,
                     response_model=ChatbotResponse)
async def create_chatbot(chatbot: ChatbotCreate,
                         user: User = Depends(current_active_user),
                         session: AsyncSession = Depends(get_async_session)):
    new_chatbot = Chatbot(name=chatbot.name,
                          llm=chatbot.llm,
                          temperature=chatbot.temperature,
                          instruction=chatbot.instruction)
    session.add(new_chatbot)
    await session.commit()
    await session.refresh(new_chatbot)

    user_chatbot = UserChatbot(user_id=user.id,
                               chatbot_id=new_chatbot.id,
                               role=UserRole.owner)
    session.add(user_chatbot)
    await session.commit()
    await session.refresh(user_chatbot)
    return ChatbotResponse.model_validate(new_chatbot)


async def get_generative_model(
    query: ChatbotQuery, session: AsyncSession = Depends(get_async_session)):
    chatbot = (await
               session.execute(select(Chatbot).where(Chatbot.id == query.id)
                               )).scalars().first()
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name=chatbot.llm,
                                  safety_settings='BLOCK_NONE',
                                  generation_config=genai.GenerationConfig(
                                      temperature=chatbot.temperature),
                                  system_instruction=chatbot.instruction)
    try:
        yield model
    finally:
        del model


@chatbot_router.post('/query')
async def get_generated_content(
    query: ChatbotQuery,
    user: User = Depends(current_active_user),
    model: genai.GenerativeModel = Depends(get_generative_model)):
    return model.generate_content(contents=query.content).text
