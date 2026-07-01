import os
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from ai.pdf_loader import extract_text
from ai.rag_pipeline import answer_question
from ai.vector_store import VectorStore
from backend.database import load_documents, save_documents

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

vector_store = VectorStore()


def ensure_index_loaded():
    if vector_store.documents:
        return

    for entry in load_documents():
        if entry.get("text"):
            vector_store.add_documents(
                [entry["text"]],
                metadata=[{"filename": entry.get("filename", "Uploaded document")}],
            )


ensure_index_loaded()


class QuestionRequest(BaseModel):
    question: str


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF")

    file_path = UPLOAD_FOLDER / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf_text = extract_text(str(file_path))
    if not pdf_text.strip():
        saved_documents = load_documents()
        entry = {
            "filename": file.filename,
            "text": "",
            "preview": "No readable text was found in the PDF",
        }

        existing_names = {doc.get("filename") for doc in saved_documents}
        if file.filename not in existing_names:
            saved_documents.append(entry)
            save_documents(saved_documents)

        return {
            "message": "PDF uploaded but no readable text could be extracted.",
            "filename": file.filename,
            "characters": 0,
            "preview": "No readable text was found in the PDF",
        }

    saved_documents = load_documents()
    entry = {
        "filename": file.filename,
        "text": pdf_text,
        "preview": pdf_text[:1000],
    }

    existing_names = {doc.get("filename") for doc in saved_documents}
    if file.filename not in existing_names:
        saved_documents.append(entry)
        save_documents(saved_documents)

    ensure_index_loaded()
    vector_store.add_documents([pdf_text], metadata=[{"filename": file.filename}])

    return {
        "message": "PDF uploaded successfully!",
        "filename": file.filename,
        "characters": len(pdf_text),
        "preview": pdf_text[:1000],
    }


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    ensure_index_loaded()
    results = vector_store.search(request.question, top_k=3)
    if not results:
        saved_docs = load_documents()
        if saved_docs:
            return {
                "answer": "I have a saved document, but I could not match your question to any readable text yet. Please try a more specific question.",
                "source": saved_docs[-1].get("filename", "Uploaded document"),
            }
        return {"answer": "Please upload a PDF first so I can answer your question.", "source": None}

    best_match = results[0]
    context_texts = [result["text"] for result in results if result.get("text")]
    answer = answer_question(request.question, context_texts)
    return {
        "answer": answer,
        "source": best_match["metadata"].get("filename", "Uploaded document"),
    }


@router.get("/documents")
def list_documents():
    return {"documents": [entry.get("filename", "Uploaded document") for entry in load_documents()]}