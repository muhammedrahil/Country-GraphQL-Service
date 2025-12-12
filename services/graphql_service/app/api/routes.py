from fastapi import APIRouter
from .controllers.countries.countries import router as countries_router

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Country GraphQL API",
        "graphql_endpoint": "/graphql",
        "graphiql": "/graphql (GET request)",
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


router.include_router(countries_router, prefix="/v1/countires", tags=["countires"])
