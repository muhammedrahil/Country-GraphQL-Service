from fastapi import APIRouter
from .controllers.notify.notify import router as notify_router

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


router.include_router(notify_router, prefix="/v1/notify", tags=["notify"])
