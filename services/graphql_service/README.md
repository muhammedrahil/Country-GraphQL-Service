# Country-GraphQL-Service
 build a production-ready GraphQL service. Let me create a comprehensive solution with two services.


alembic revision --autogenerate -m "init"
alembic upgrade head
uvicorn app.main:app --reload