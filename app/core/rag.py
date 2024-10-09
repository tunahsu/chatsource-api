from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.chatbots import ChatbotQueryRequest
from app.models import Chatbot, Document
from app.core.db import get_async_session
from app.core.config import settings

import openai
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings, Document as LIDocument

openai.api_key = settings.OPENAI_API_KEY

# Global model settings
Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small')


async def get_query_engine(query: ChatbotQueryRequest,
                           session: AsyncSession = Depends(get_async_session)):
    chatbot = (await
               session.execute(select(Chatbot).where(Chatbot.id == query.id)
                               )).scalars().first()
    docs = (await session.execute(
        select(Document).join(Chatbot).filter(
            Document.chatbot_id == chatbot.id))).scalars().all()
    documents = [
        LIDocument(text=doc.content, metadata={
            'title': doc.title,
        }) for doc in docs
    ]
    llm = OpenAI(model=chatbot.llm,
                 temperature=chatbot.temperature,
                 system_prompt=chatbot.instruction)
    index = VectorStoreIndex(documents, show_progress=True)
    query_engine = index.as_query_engine(llm=llm)
    try:
        yield query_engine
    finally:
        del query_engine
