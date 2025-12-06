from sqlalchemy.orm import Session
from sqlalchemy import func
from movie_assistant.models.collection import (
    Collection,
    Document,
    CollectionDocument,
    ChunkEmbedding,
)
from fastapi import HTTPException, status, UploadFile
from uuid import UUID
from movie_assistant.llm.utils import chunk_text_with_overlap
from PyPDF2 import PdfReader
from movie_assistant.core.config import settings
from openai import OpenAI
from movie_assistant.schemas.collection import (
    CollectionBase,
    ViewCollection,
)


class CollectionRepository:

    @staticmethod
    def add_collection(collection_info: CollectionBase, db: Session) -> ViewCollection:
        collection_name = collection_info.name
        collection_exists = (
            db.query(Collection)
            .filter(func.lower(Collection.name) == collection_name.lower())
            .first()
        )
        if collection_exists:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                detail=f"Collection with name {collection_name} already exists.",
            )

        new_collection = Collection(name=collection_name)
        db.add(new_collection)
        db.commit()
        db.refresh(new_collection)
        return new_collection

    @staticmethod
    def get_collection(collection_id: UUID, db: Session) -> list[ViewCollection]:
        collection_exists = (
            db.query(Collection).filter(Collection.id == collection_id).first()
        )
        if collection_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Collection not found.",
            )

        return [collection_exists]

    @staticmethod
    def get_all_collection(db: Session) -> list[ViewCollection]:
        collection_info = db.query(Collection).filter(Collection.is_active).all()

        return collection_info

    @staticmethod
    def ingest_document(collection_id: int, document: UploadFile, db: Session):
        collection_exists = (
            db.query(Collection).filter(Collection.id == collection_id).first()
        )
        if collection_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Collection with ID {collection_id} doesn't exists.",
            )
        print("Document Summary Generation Started :")
        reader = PdfReader(document.file)
        client = OpenAI(
            api_key=settings.NVIDIA_API_KEY, base_url=settings.NVIDIA_BASE_URL
        )
        new_document = Document(name=document.filename)
        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        link = CollectionDocument(
            collection_id=collection_id, document_id=new_document.id
        )
        db.add(link)
        db.commit()
        db.refresh(link)

        print("Document Embedding creation started :")

        """
        Page Chunk wise embedder
        """
        buffer = ""
        chunk_size = 512
        overlap = 50
        reader = PdfReader(document.file)
        for page_no, page in enumerate(reader.pages, start=1):
            print(f"Page No. {page_no} embedding generation in progress...")
            page_text = page.extract_text()
            if not page_text:
                continue

            text_to_chunk = buffer + page_text

            chunks, buffer = chunk_text_with_overlap(text_to_chunk, chunk_size, overlap)
            embedding_completion = client.embeddings.create(
                model=settings.EMBEDDING_MODEL,
                input=chunks,
                encoding_format="float",
                extra_body={"input_type": "passage", "truncate": "NONE"},
            )
            page_embeddings = embedding_completion.data
            for chunk_idx, page_embedding in enumerate(page_embeddings):
                new_document_embedding = ChunkEmbedding(
                    collection_document_id=link.id,
                    chunk=chunks[chunk_idx],
                    embedding=page_embedding.embedding,
                    source_info={
                        "chunk_index": chunk_idx,
                        "page_no": page_no,
                        "document_name": new_document.name,
                    },
                )
                db.add(new_document_embedding)

        """
        Page Chunk wise embedder end
        """
        db.commit()

        response = {
            "document_id": new_document.id,
            "collection_id": collection_id,
            "document_name": new_document.name,
            "total_pages": len(reader.pages),
        }
        return response
