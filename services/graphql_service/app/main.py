from fastapi import FastAPI
from app.settings import settings
from app.api.routes import api_router
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    # Create FastAPI App
    fast_api_app = FastAPI(
        title=settings.app_name,
        description="GraphQL API for country data with geospatial queries",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fast_api_app.include_router(api_router, prefix="")
    # fast_api_app.add_middleware(ConnectionPoolMonitorMiddleware, engine=engine)

    return fast_api_app


# Initialize the app
app = create_app()
