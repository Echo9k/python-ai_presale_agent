import os
from sanic import Blueprint, response
from sanic.request import Request
from sanic_ext import openapi
from utils.milvus_connector import get_milvus_vectorstore, ensure_collection_exists
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sanic.log import logger

bp = Blueprint("documents", url_prefix="/documents")

# Ensure collection exists at startup
doc_vs = ensure_collection_exists()

@bp.get("")
@openapi.summary("List all uploaded documents")
async def list_documents(request: Request):
    # Query Milvus for all unique filenames in metadata
    # LangChain doesn't provide a direct way, so we use the underlying client
    client = doc_vs._connection
    expr = ""
    output_fields = ["filename"]
    results = client.query(
        collection_name=doc_vs._collection_name,
        expr=expr,
        output_fields=output_fields
    )
    filenames = list({r["filename"] for r in results})
    return response.json({"files": filenames})

@bp.post("")
@openapi.summary("Upload a document and store its vectors in Milvus")
async def upload_document(request: Request):
    if not request.files or "file" not in request.files:
        return response.json({"error": "No file uploaded"}, status=400)
    file = request.files["file"]
    filename = file.name
    content = file.body.decode("utf-8")
    # Save to temp file for loader
    temp_path = f"/tmp/{filename}"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(content)
    # Load, split, embed, and store
    loader = TextLoader(temp_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    # Add filename as metadata
    for d in splits:
        d.metadata["filename"] = filename
    doc_vs.add_documents(splits)
    os.remove(temp_path)
    logger.info(f"Uploaded and stored {filename}")
    return response.json({"message": f"Stored {filename}"})

@bp.delete("/<filename:str>")
@openapi.summary("Delete all vectors for a document by filename")
async def delete_document(request: Request, filename: str):
    # Delete all vectors with this filename in metadata
    client = doc_vs._connection
    expr = f'filename == "{filename}"'
    client.delete(collection_name=doc_vs._collection_name, expr=expr)
    logger.info(f"Deleted vectors for {filename}")
    return response.json({"message": f"Deleted {filename}"})
