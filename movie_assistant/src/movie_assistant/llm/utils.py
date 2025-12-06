from openai import OpenAI
from movie_assistant.core.config import settings
from fastapi import UploadFile
from PyPDF2 import PdfReader
from sqlalchemy.orm import Session
from uuid import UUID
from movie_assistant.models.collection import (
    ChunkEmbedding,
    Document,
    CollectionDocument,
)


def create_embeddings(chunks_list: list[str]):
    client = OpenAI(api_key=settings.NVIDIA_API_KEY, base_url=settings.NVIDIA_BASE_URL)
    response = client.embeddings.create(
        input=chunks_list,
        model=settings.EMBEDDING_MODEL,
        encoding_format="float",
        extra_body={"input_type": "passage", "truncate": "NONE"},
    )
    print(response.data)

    return response.data


def split_into_chunks(text: str, chunk_size: int = 300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks


def chunk_text_with_overlap(text, chunk_size=512, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)

    while start + chunk_size <= text_length:
        chunk = text[start : start + chunk_size]
        chunks.append(chunk)
        start += chunk_size - overlap

    buffer = text[start:]
    return chunks, buffer


def process_document(document: UploadFile, collection_id: UUID, db: Session):
    reader = PdfReader(document.file)
    new_document = Document(name=document.filename)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    new_document_collection = CollectionDocument(
        collection_id=collection_id, document_id=new_document.id
    )
    db.add(new_document_collection)
    db.commit()
    db.refresh(new_document_collection)

    for page_no, page in enumerate(reader.pages, start=1):
        chunks_list = split_into_chunks(page.extract_text())
        embeddings_list = create_embeddings(chunks_list)
        for idx, embedding in enumerate(embeddings_list):
            chunk_metadata = {
                "chunk_no": idx + 1,
                "document_name": document.filename,
                "page_no": page_no,
            }
            new_embedding = ChunkEmbedding(
                collection_document_id=new_document_collection.id,
                embedding=embedding.embedding,
                chunk=chunks_list[idx],
                chunk_metadata=chunk_metadata,
            )
            db.add(new_embedding)
            db.commit()
    response = "Embeddings generated successfully."
    return response
