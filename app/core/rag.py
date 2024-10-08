import os

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.chatbots import ChatbotQueryRequest
from app.models import Chatbot, Document
from app.core.db import get_async_session
from app.core.config import settings

os.environ['GOOGLE_API_KEY'] = settings.GEMINI_API_KEY
from llama_index.llms.gemini import Gemini
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings, PromptTemplate, Document as LIDocument
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# global
Settings.embed_model = HuggingFaceEmbedding(
    model_name='intfloat/multilingual-e5-small')


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
    llm = Gemini(model=f'models/{chatbot.llm}',
                 temperature=chatbot.temperature)
    index = VectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine(llm=llm)
    try:
        yield query_engine
    finally:
        del query_engine
