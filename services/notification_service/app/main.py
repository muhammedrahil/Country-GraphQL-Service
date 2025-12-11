from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.notification_service.app.settings import settings
from services.notification_service.app.api.routes import router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    # Create FastAPI App
    fast_api_app = FastAPI(
        title=settings.app_name,
        description="Notication for GraphQL country",
        version="1.0.0",
    )
    fast_api_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fast_api_app.include_router(router, prefix="")

    return fast_api_app


# Initialize the app
app = create_app()
