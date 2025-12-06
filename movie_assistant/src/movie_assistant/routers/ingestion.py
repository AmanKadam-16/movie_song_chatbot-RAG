from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Query,
    File,
    Form,
    UploadFile,
)
from movie_assistant.schemas import collection as collection_schema
from movie_assistant.utils.auth import get_current_user, authorize_role
from typing import Annotated
from sqlalchemy.orm import Session
from uuid import UUID
from movie_assistant.database.deps import get_db
from movie_assistant.schemas.app_enums import Role
from movie_assistant.services import collection as collection_service


router = APIRouter(
    prefix="/collection",
    tags=["collection"],
    dependencies=[Depends(authorize_role([Role.ADMIN.value]))],
)


@router.post("", response_model=collection_schema.ViewCollection)
def add_collection(
    collection_info: collection_schema.CollectionBase,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        service_response = collection_service.add_collection(
            collection_info=collection_info, db=db
        )
        return service_response
    except HTTPException as he:
        raise HTTPException(
            status_code=he.status_code, detail=f"HTTP Error : {he.detail}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error : {e}",
        )


@router.get("/", response_model=list[collection_schema.ViewCollection])
def get_collection(
    collection_id: UUID = None,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        service_response = collection_service.get_collection_info(
            collection_id=collection_id, db=db
        )
        return service_response
    except HTTPException as he:
        raise HTTPException(
            status_code=he.status_code, detail=f"HTTP Error : {he.detail}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error : {e}",
        )


@router.post("/document")
def add_document(
    collection_id: Annotated[UUID, Form()],
    document_file: Annotated[UploadFile, File()],
    db=Depends(get_db),
):
    try:
        service_response = collection_service.add_document(
            document=document_file, collection_id=collection_id, db=db
        )
        return service_response
    except HTTPException as he:
        raise HTTPException(
            status_code=he.status_code, detail=f"HTTP Error : {he.detail}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server Error : {e}",
        )
