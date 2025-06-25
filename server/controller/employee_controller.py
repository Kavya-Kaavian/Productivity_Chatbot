from services.employee_embedding_service import process_employee_csv_service

async def process_csv_controller(file_path: str):
    return await process_employee_csv_service(file_path)
