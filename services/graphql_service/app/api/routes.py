from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Country GraphQL API",
        "graphql_endpoint": "/graphql",
        "graphiql": "/graphql (GET request)",
    }


@api_router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
