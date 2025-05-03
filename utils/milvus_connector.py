from langchain_milvus.vectorstores.zilliz import Zilliz
from langchain_huggingface import HuggingFaceEmbeddings
from utils.config import settings


# You can change this to your preferred embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Milvus collection name
COLLECTION_NAME = "documents"


def get_milvus_vectorstore():
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    # Use the endpoint and token from .env
    vectorstore = Zilliz(
        embedding_function=embedding,
        connection_args={
            "uri": settings.ZILLIZ_ENDPOINT,
            "token": settings.ZILLIZ_TOKEN,
            "secure": True,
        },
        collection_name=COLLECTION_NAME,
    )
    return vectorstore


def ensure_collection_exists():
    # This will create the collection if it doesn't exist
    vs = get_milvus_vectorstore()
    return vs
