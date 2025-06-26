from services.retriever_service import search_by_query_service

async def search_controller(query: str, top_k: int = 5):
    return await search_by_query_service(query, top_k)
