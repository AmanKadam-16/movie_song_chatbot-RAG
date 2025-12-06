from movie_assistant.repository.collection import CollectionRepository
from movie_assistant.schemas import collection as collection_schema
from sqlalchemy.orm import Session
from fastapi import UploadFile
from uuid import UUID


def add_collection(
    collection_info: collection_schema.CollectionBase, db: Session
) -> collection_schema.ViewCollection:
    collection_added = CollectionRepository.add_collection(
        collection_info=collection_info, db=db
    )
    return collection_added


def get_collection_info(
    db: Session, collection_id: UUID = None
) -> list[collection_schema.ViewCollection]:
    collection_info = []
    if collection_id:
        collection_info = CollectionRepository.get_collection(
            collection_id=collection_id, db=db
        )
    else:
        collection_info = CollectionRepository.get_all_collection(db=db)
    return collection_info


def add_document(document: UploadFile, collection_id: UUID, db: Session):

    embeddings_result = CollectionRepository.ingest_document(
        document=document, collection_id=collection_id, db=db
    )
    return embeddings_result
