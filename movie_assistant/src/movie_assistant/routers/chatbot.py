from fastapi import APIRouter, HTTPException, status
from movie_assistant.services import chatbot as chatbot_service
from movie_assistant.schemas.chatbot import ChatInput
from movie_assistant.utils.auth import authorize_role
from movie_assistant.schemas.app_enums import Role
from fastapi import Depends
from movie_assistant.database.deps import get_db

router = APIRouter(
    prefix="/chat",
    tags=["chatbot"],
    dependencies=[Depends(authorize_role([Role.ADMIN.value, Role.USER.value]))],
)


@router.post("")
def conversate(user_input: ChatInput, db=Depends(get_db)):
    try:
        service_response = chatbot_service.conversate(user_input=user_input, db=db)
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


@router.get("/{session_id}")
def retrieve_session(): ...


@router.get("/history")
def chat_history(): ...
