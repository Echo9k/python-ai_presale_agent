from langchain_community.vectorstores import Milvus
from langchain.embeddings import HuggingFaceEmbeddings
from utils.config import settings

# You can change this to your preferred embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Milvus collection name
COLLECTION_NAME = "documents"


def get_milvus_vectorstore():
    # Set up the embedding function
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Connect to Milvus (Zilliz Cloud)
    vectorstore = Milvus(
        embedding_function=embedding,
        connection_args={
            "uri": f"https://{settings.ZILLIZ_CLUSTER_ID}.gcp-us-west1.zillizcloud.com:19530",
            "user": settings.ZILLIZ_USER,
            "password": settings.ZILLIZ_PASSWORD,
            "secure": True,
        },
        collection_name=COLLECTION_NAME,
    )
    return vectorstore


def ensure_collection_exists():
    # This will create the collection if it doesn't exist
    vs = get_milvus_vectorstore()
    return vs
