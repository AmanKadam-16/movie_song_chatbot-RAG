from tavily import TavilyClient
from movie_assistant.core.config import settings
from movie_assistant.database.deps import get_db
from movie_assistant.llm.utils import create_embeddings
from movie_assistant.models.collection import ChunkEmbedding
from sqlalchemy.orm import Session


def rag_search(arg: dict):
    print("rag tool called")
    user_query = arg.get("user_query")
    db: Session = next(get_db())
    user_query_embeddings = create_embeddings([user_query])

    cos_distance = ChunkEmbedding.embedding.cosine_distance(
        user_query_embeddings[0].embedding
    )
    cos_sim = 1 - cos_distance
    top_k = 5

    similar_chunks = db.query(ChunkEmbedding).order_by(cos_distance).limit(top_k).all()

    similar_chunk_list = []
    for chunk in similar_chunks:
        print()
        row = {"chunk": chunk.chunk, "chunk_metadata": chunk.chunk_metadata}
        similar_chunk_list.append(row)

    # print(similar_chunk_list)

    return similar_chunk_list


def web_search(arg: dict):
    print("web search tool called.")
    user_query = arg.get("search_query")
    client = TavilyClient(settings.TAVILY_API)
    response = client.search(query=user_query, search_depth="basic")
    return response
