from fastapi import APIRouter
from .controllers.countries.countries import router as countries_router
from app.graphiql import graphiql_html

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


@router.get("/graphiql")
async def graphiql_ui():
    return graphiql_html()


router.include_router(countries_router, prefix="/v1/countires", tags=["countires"])
