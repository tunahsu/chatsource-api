import uuid
import google.generativeai as genai
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from models import User, Chatbot
from schemas.chatbots import ChatbotCreate, ChatbotUpdate, ChatbotRequest, ChatbotResponse
from oauth2 import get_current_user
from exception import NewHTTPException

chatbot_router = APIRouter(prefix='/chatbots', tags=['Chatbots'])


@chatbot_router.post('/', response_model=ChatbotResponse)
async def create_chatbot(chatbot: ChatbotCreate,
                         current_user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if any(chatbot.chatbot_name == c.chatbot_name
           for c in current_user.chatbots):
        raise NewHTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail='Chatbot name already used')
    chatbot_id = f'{chatbot.chatbot_name}-{uuid.uuid4().hex[:8]}'
    new_chatbot = Chatbot(chatbot_id=chatbot_id,
                          chatbot_name=chatbot.chatbot_name,
                          llm_name=chatbot.llm_name,
                          llm_api_key=chatbot.llm_api_key,
                          temperature=chatbot.temperature,
                          instructions=chatbot.instructions,
                          user_id=current_user.id)
    db.add(new_chatbot)
    db.commit()
    db.refresh(new_chatbot)
    yield ChatbotResponse.model_validate(new_chatbot)


async def get_generative_model(chatbot: ChatbotRequest):
    genai.configure(api_key=chatbot.llm_api_key)
    yield genai.GenerativeModel(chatbot.llm_name)



@chatbot_router.post('/query')
async def get_generated_content(chatbot: ChatbotRequest, model = Depends(get_generative_model)):
   query = chatbot.query
   return model.generate_content(query).text
