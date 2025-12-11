from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Country GraphQL Notification API",
        "graphql_endpoint": "/graphql",
        "graphiql": "/graphql (GET request)",
    }


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
