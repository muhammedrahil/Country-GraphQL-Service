# Country-GraphQL-Service
 build a production-ready GraphQL service. Let me create a comprehensive solution with two services.


alembic -c services/graphql_service/alembic.ini revision --autogenerate -m "init"
alembic -c services/graphql_service/alembic.ini upgrade head
uvicorn services.graphql_service.app.main:app --reload