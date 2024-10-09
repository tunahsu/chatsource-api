from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from llama_index.core.base.base_query_engine import BaseQueryEngine

from app.schemas.chatbots import ChatbotCreateRequest, ChatbotCreateResponse, ChatbotQueryRequest, ChatbotTrainRequest, ChatbotTrainReponse
from app.models import User, Chatbot, UserRole, UserChatbot, Document
from app.core.db import get_async_session
from app.core.users import current_active_user
from app.core.exception import NewHTTPException
from app.core.rag import get_query_engine

chatbot_router = APIRouter(prefix='/chatbots', tags=['Chatbots'])


@chatbot_router.get('/list', response_model=list[dict])
async def get_chatbot_list(user: User = Depends(current_active_user),
                           session: AsyncSession = Depends(get_async_session)):
    print('XD')
    chatbots_list = []
    chatbots = (await session.execute(
        select(Chatbot).join(UserChatbot).filter(
            UserChatbot.user_id == user.id))).scalars().all()
    for chatbot in chatbots:
        user_chatbots = (await session.execute(
            select(UserChatbot).join(User).filter(
                UserChatbot.chatbot_id == chatbot.id))).scalars().all()
        chatbot_dict = ChatbotCreateResponse.model_validate(
            chatbot).model_dump()
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
                     status_code=status.HTTP_201_CREATED,
                     response_model=ChatbotCreateResponse)
async def create_chatbot(chatbot: ChatbotCreateRequest,
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
    return ChatbotCreateResponse.model_validate(new_chatbot)


@chatbot_router.post('/query', response_model=str)
async def get_generated_content(
    query: ChatbotQueryRequest,
    user: User = Depends(current_active_user),
    query_engine: BaseQueryEngine = Depends(get_query_engine)):

    return str(await query_engine.aquery(query.content))


@chatbot_router.post('/train', status_code=status.HTTP_201_CREATED)
async def train_from_text(doc: ChatbotTrainRequest,
                          user: User = Depends(current_active_user),
                          session: AsyncSession = Depends(get_async_session)):
    new_doc = Document(**doc.model_dump())
    session.add(new_doc)
    await session.commit()
    await session.refresh(new_doc)
    return ChatbotTrainReponse.model_validate(new_doc)
