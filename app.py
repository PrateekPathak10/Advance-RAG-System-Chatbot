from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import shutil
import os
import threading

from langchain_chroma import Chroma

from Ingestion.embedder import get_embedded
from Ingestion.loader import load_pdf
from Ingestion.chunks import split_docs

from Generation.llm import get_llm
from pipeline.rag_pipeline import run_rag_pipeline


UPLOAD_DIR = "uploaded_docs"
DB_DIR = "./db"
PORT = int(os.environ.get("PORT", 10000))

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

vector_db = None
embeddings = None
llm = None
all_docs = []
processing_status = {}


def get_embeddings():
    global embeddings
    if embeddings is None:
        embeddings = get_embedded()  
    return embeddings


def get_vector_db():
    global vector_db
    if vector_db is None:
        vector_db = Chroma(
            persist_directory=DB_DIR,
            embedding_function=get_embeddings()
        )
    return vector_db


def get_llm_instance():
    global llm
    if llm is None:
        llm = get_llm()
    return llm


def stream_response(text):
    for word in text.split():
        yield word + " "


def background_ingest(file_path, filename):
    global processing_status, all_docs

    processing_status[filename] = "processing"

    try:
        docs = load_pdf(file_path)
        chunks = split_docs(docs)

        chunks = chunks[:200]

        db = get_vector_db()

        fast_chunks = chunks[:100]
        db.add_documents(fast_chunks)
        all_docs.extend(fast_chunks)

        processing_status[filename] = "ready_partial"

        remaining = chunks[100:]

        batch_size = 16
        for i in range(0, len(remaining), batch_size):
            batch = remaining[i:i+batch_size]
            db.add_documents(batch)
            all_docs.extend(batch)

        processing_status[filename] = "done"

    except Exception as e:
        processing_status[filename] = f"error: {str(e)}"


@app.get("/ask")
async def ask(query: str):
    return run_rag_pipeline(
        query,
        get_llm_instance(),
        get_vector_db(),
        all_docs
    )


@app.get("/ask-stream")
async def ask_stream(query: str):
    try:
        result = run_rag_pipeline(
            query,
            get_llm_instance(),
            get_vector_db(),
            all_docs
        )

        return StreamingResponse(
            stream_response(result["answer"]),
            media_type="text/plain"
        )

    except Exception as e:
        return {"error": str(e)}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_bytes = await file.read()

    if len(file_bytes) > 3 * 1024 * 1024:
        return {"error": "File too large (max 3MB for demo)"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)

    threading.Thread(
        target=background_ingest,
        args=(file_path, file.filename)
    ).start()

    return {
        "message": "Upload successful, processing started",
        "file": file.filename
    }


@app.get("/status")
async def get_status(filename: str):
    return {
        "status": processing_status.get(filename, "not_found")
    }


@app.get("/documents")
async def list_documents():
    return {"documents": os.listdir(UPLOAD_DIR)}