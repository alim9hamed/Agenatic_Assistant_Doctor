from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.factories import LLMProviderFactory
from stores.llm.factories import EmbeddingProviderFactory
from stores.vectordb import VectorDBProviderFactory
from stores.llm.templates import TemplateParser

app = FastAPI()


async def startup_span():
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)
    embedding_provider_factory = EmbeddingProviderFactory(settings)
    vector_provider_factory = VectorDBProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(
        provider=settings.GENERATION_BACKEND
    )

    app.generation_client.set_generation_model(
        model_id=settings.GENERATION_MODEL_ID
    )

    # embedding client
    app.embedding_client = embedding_provider_factory.create(
        provider=settings.EMBEDDING_BACKEND
    )

    app.embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_MODEL_SIZE
    )

    # vector db client
    app.vectordb_client = vector_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )

    app.vectordb_client.connect()

    # template parser
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )

async def shutdown_span():
    app.mongo_conn.close()
    app.vectordb_client.disconnect()


app.router.on_startup.append(startup_span)
app.router.on_shutdown.append(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

