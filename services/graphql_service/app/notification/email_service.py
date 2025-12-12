import httpx

from app.settings import settings


async def notify_email_service(country_data: dict):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(
                f"{settings.notification_service}/v1/notify/country-added",
                json=country_data,
            )
            response.raise_for_status()
            print("Email service notified successfully")
        except Exception as e:
            print(f"Failed to notify email service: {e}")
