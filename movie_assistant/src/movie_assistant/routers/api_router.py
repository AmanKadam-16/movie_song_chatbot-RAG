from movie_assistant.routers.chatbot import router as chatbot_router
from movie_assistant.routers.auth import router as auth_router
from movie_assistant.routers.ingestion import router as ingestion_router
from fastapi import APIRouter


router = APIRouter()

router.include_router(auth_router)
router.include_router(chatbot_router)
router.include_router(ingestion_router)
