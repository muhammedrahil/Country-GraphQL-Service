# Country GraphQL Services

This project consists of **two microservices** that work together to provide a complete Country GraphQL API solution with notification capabilities.

## 📋 Project Overview

The Country GraphQL project is a microservices-based application that provides:
- A comprehensive GraphQL API for querying country information
- Geospatial queries to find nearby countries
- Email notification service for administrative alerts

## 🏗️ Architecture

The project is organized into two independent services:

### 1. **GraphQL Service** 
A GraphQL API that provides access to country data including population, area, languages, and geospatial information. It supports querying, mutations, and automatic data ingestion from external sources.

📖 **[Read GraphQL Service Documentation →](./services/graphql_service/README.md)**

**Key Features:**
- GraphQL API with interactive playground
- Country data queries with pagination
- Geospatial queries (find nearby countries)
- Create/update country information
- PostgreSQL database with PostGIS support
- Automatic data ingestion

### 2. **Notification Service**
A dedicated service for handling email notifications and alerts. This service is triggered when certain events occur in the GraphQL service (e.g., new country creation).

📖 **[Read Notification Service Documentation →](./services/notification_service/README.md)**

**Key Features:**
- Email notification handling
- SMTP integration
- Admin alert system
- RESTful API endpoints

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **PostgreSQL** (with PostGIS extension for GraphQL service)
- **Poetry** (Python dependency manager)

### Running Both Services

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd services
   ```

2. **Set up GraphQL Service:**
   ```bash
   cd graphql_service
   poetry install
   # Configure .env file (see graphql_service/README.md)
   poetry run alembic upgrade head
   poetry run uvicorn app.main:app --reload --port 8000
   ```

3. **Set up Notification Service:**
   ```bash
   cd ../notification_service
   poetry install
   # Configure .env file (see notification_service/README.md)
   poetry run uvicorn app.main:app --reload --port 8001
   ```

The services will be available at:
- **GraphQL Service**: `http://localhost:8000` (GraphQL Playground: `http://localhost:8000/graphql`)
- **Notification Service**: `http://localhost:8001`

## 📚 Documentation

For detailed setup, configuration, and usage instructions, please refer to the individual service README files:

| Service | Documentation |
|---------|--------------|
| GraphQL Service | [📖 View README](./services/graphql_service/README.md) |
| Notification Service | [📖 View README](./services/notification_service/README.md) |

## 🛠️ Technology Stack

- **Framework:** FastAPI
- **GraphQL:** Graphene
- **Database:** PostgreSQL (with PostGIS for geospatial queries)
- **ORM:** SQLAlchemy (async)
- **Email:** SMTP
- **Dependency Management:** Poetry
- **Migrations:** Alembic

## 🔗 Service Communication

The GraphQL Service communicates with the Notification Service to send email alerts when:
- A new country is added to the database
- Administrative actions require notification

## 📝 License

This project is part of the Country GraphQL Service suite.
