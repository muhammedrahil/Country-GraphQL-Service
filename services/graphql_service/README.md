# Country GraphQL Service

This is a **GraphQL API** service that provides information about countries. It allows you to query country details like population, area, languages, and more. It also supports **geospatial queries** to find countries near a specific location.

The service automatically fetches (ingests) country data from external sources to keep the database up-to-date.

## Prerequisites

Before you start, make sure you have these installed on your computer:

*   **Python 3.10** or higher
*   **PostgreSQL** (Database)
*   **Poetry** (For managing Python packages)

## Installation & Setup

Follow these steps to set up the project locally:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd services/graphql_service
    ```

2.  **Install dependencies:**
    We use `poetry` to manage dependencies. Run this command to install them:
    ```bash
    poetry install
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the `services/graphql_service` directory. You can copy the example below:
    ```env
    # Database Configuration
    DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/country_db

    # Email Notification Configuration
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USERNAME=your_email@gmail.com
    SMTP_PASSWORD=your_app_password
    FROM_EMAIL=your_email@gmail.com
    ADMIN_EMAILS=admin1@example.com,admin2@example.com
    ```
    *Replace the values with your actual configuration.*

## Database Migrations

To set up the database tables, run the migration command:

```bash
poetry run alembic upgrade head
```

This will create the necessary tables in your PostgreSQL database.

## Running the Application

To start the server locally, run:

```bash
poetry run uvicorn app.main:app --reload
```

*   The API will be running at: `http://localhost:8000`
*   You can access the **GraphQL Playground** to test queries at: `http://localhost:8000/graphql`

## How to Use

Once the server is running, go to `http://localhost:8000/graphql` in your browser. You will see an interactive playground where you can write GraphQL queries.

**Example Queries:**

Here are some example queries you can run in the playground:

**1. Get a list of countries (with pagination):**
```graphql
query {
  countriesList(limit: 5, after: "") {
    edges {
        node {
            name
            alpha2Code
            capital
            population
            region
        }
    }
    pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
        endCursor
    }
    totalCount
  }
}
```

**2. Get a single country by code:**
```graphql
query {
  getCountry(countryCode: "US") {
    name
    capital
    currency
    languages
  }
}
```

**3. Find nearby countries:**
```graphql
query {
  nearbyCountries(latitude: 48.8566, longitude: 2.3522, radiusKm: 1000) {
    name
    capital
  }
}
```

**4. Create a new country:**

> [!NOTE]
> When a new country is successfully created, an email notification will be automatically sent to the admin.

```graphql
mutation {
  addCountry(input: {
    name: "New Country"
    alpha2Code: "NC"
    alpha3Code: "NCY"
    capital: "New City"
    population: 1000000
    region: "Europe"
  }) {
    success
    message
  }
}
```