from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from movie_assistant.routers.api_router import router as master_router
from movie_assistant.utils.startup.startup_utils import seed_admin

app = FastAPI(
    title="Movie and Song Chatbot",
    description="""Capable of answering based on wide knowledge base of movie and 
    songs and ability to perform web search if required.""",
)
app.include_router(master_router)


@app.get("/")
def root():
    print(seed_admin())
    return JSONResponse(status_code=status.HTTP_200_OK, content="System Operational.")
