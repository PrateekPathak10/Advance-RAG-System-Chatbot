from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import shutil
import os
import threading
from langchain_chroma import Chroma
from Ingestion.embedder import get_embedded
from Ingestion.ingest_pipeline import ingest_pdf
from Ingestion.loader import load_pdf
from Ingestion.chunks import split_docs
from Generation.llm import get_llm
from pipeline.rag_pipeline import run_rag_pipeline


#CONFIG
UPLOAD_DIR = "uploaded_docs"
DB_DIR = "./db"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

#INIT
embeddings = get_embedded()

vector_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

all_docs = []
processing_status = {}

llm = get_llm()

#STREAM HELPER
def stream_response(text):
    for word in text.split():
        yield word + " "

#BACKGROUND INGEST
def background_ingest(file_path, filename):
    global processing_status, vector_db, all_docs

    processing_status[filename] = "processing"

    docs = load_pdf(file_path)
    chunks = split_docs(docs)

    fast_chunks = chunks[:200]

    vector_db.add_documents(fast_chunks)
    all_docs.extend(fast_chunks)

    processing_status[filename] = "ready_partial"

    remaining = chunks[200:]

    if remaining:
        batch_size = 64
        for i in range(0, len(remaining), batch_size):
            batch = remaining[i:i+batch_size]
            vector_db.add_documents(batch)
            all_docs.extend(batch)

    processing_status[filename] = "done"


#ASK
@app.get("/ask")
async def ask(query: str):
    return run_rag_pipeline(query, llm, vector_db, all_docs)


@app.get("/ask-stream")
async def ask_stream(query: str):

    try:
        result = run_rag_pipeline(query, llm, vector_db, all_docs)

        return StreamingResponse(
            stream_response(result["answer"]),
            media_type="text/plain"
        )

    except Exception as e:
        return {"error": str(e)}


#UPLOAD
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    threading.Thread(
        target=background_ingest,
        args=(file_path, file.filename)
    ).start()

    return {
        "message": "Upload successful, processing started",
        "file": file.filename
    }


#STATUS 
@app.get("/status")
async def get_status(filename: str):
    return {
        "status": processing_status.get(filename, "not_found")
    }



@app.get("/documents")
async def list_documents():
    return {"documents": os.listdir(UPLOAD_DIR)}