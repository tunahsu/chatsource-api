import google.generativeai as genai

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chatbots import ChatbotCreate, ChatbotRequest, ChatbotResponse
from app.models import User, Chatbot
from app.core.db import get_async_session
from app.core.users import current_active_user
from app.core.exception import NewHTTPException

chatbot_router = APIRouter(prefix='/chatbots', tags=['Chatbots'])


@chatbot_router.post('/', status_code=201, response_model=ChatbotResponse)
async def create_chatbot(chatbot: ChatbotCreate,
                         user: User = Depends(current_active_user),
                         session: AsyncSession = Depends(get_async_session)):
    new_chatbot = Chatbot(name=chatbot.name,
                          llm=chatbot.llm,
                          api_key=chatbot.api_key,
                          temperature=chatbot.temperature,
                          instruction=chatbot.instruction,
                          user_id=user.id)
    session.add(new_chatbot)
    await session.commit()
    await session.refresh(new_chatbot)
    return ChatbotResponse.model_validate(new_chatbot)


async def get_generative_model(chatbot: ChatbotRequest):
    genai.configure(api_key=chatbot.api_key)
    yield genai.GenerativeModel(chatbot.name)


@chatbot_router.post('/query')
async def get_generated_content(chatbot: ChatbotRequest,
                                user: User = Depends(current_active_user),
                                model=Depends(get_generative_model)):
    query = chatbot.query
    return model.generate_content(query).text
