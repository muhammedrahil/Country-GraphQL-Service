# Country GraphQL Notification Service

This is a simple notification service for the Country GraphQL project. It handles sending emails and notifications.

## Prerequisites

Before you start, make sure you have the following installed:

- **Python**: Version 3.10 or higher.
- **Poetry**: A tool for dependency management in Python.

## Installation

1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the service directory**:
    ```bash
    cd services/notification_service
    ```
3.  **Install dependencies**:
    ```bash
    poetry install
    ```

## Configuration

You need to set up some environment variables to make the service work. Create a file named `.env` in the `services/notification_service` directory and add the following:

```env
APP_NAME="Country GraphQL Notification Service"
SMTP_HOST="your_smtp_host"
SMTP_PORT="your_smtp_port"
SMTP_USERNAME="your_smtp_username"
SMTP_PASSWORD="your_smtp_password"
FROM_EMAIL="your_email@example.com"
ADMIN_EMAIL="admin@example.com"
```

*Note: Replace the values with your actual email server details.*

## How to Run

To start the application, run the following command:

```bash
poetry run uvicorn app.main:app --reload
```

The service will start running, and you can access it at `http://127.0.0.1:8000`.