from fastapi import APIRouter

from app.schema.main import CountryNotification
from app.utils.exceptions import BadRequest
from app.utils.response import Response

router = APIRouter()


@router.post("/notify/country-added")
async def notify_country_added(notification: CountryNotification):
    """Endpoint to receive country added notifications."""
    try:
        # email_service.send_country_added_notification(notification.dict())
        return Response(message="Notification sent to admins", status=200)
    except Exception as e:
        raise BadRequest(detail=str(e))
