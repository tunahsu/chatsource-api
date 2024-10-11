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
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import VectorStoreIndex, Settings, Document as LIDocument
from llama_index.core.retrievers import VectorIndexRetriever

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
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3,
    )
    query_engine = RetrieverQueryEngine.from_args(retriever=retriever, llm=llm)
    try:
        yield query_engine
    finally:
        del query_engine
