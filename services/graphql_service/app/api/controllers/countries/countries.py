from fastapi import APIRouter

from ingestion_service.ingestion import CountryIngestionService

router = APIRouter()


@router.post("/run_periodic_ingestion")
async def run_periodic_ingestion():
    service = CountryIngestionService()
    try:
        stats = await service.run_ingestion()
    except Exception as e:
        print(f"Periodic ingestion error: {e}")
    return {"stats": stats}
