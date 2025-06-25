# server/controller/getEmployeeData.py

from services.getEmployeeData import search_vector_db  # ✅ Correct import

async def getDataFromDb(query: str):
    return search_vector_db(query)  # ✅ No await since it’s a sync function
