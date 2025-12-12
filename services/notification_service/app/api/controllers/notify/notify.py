from fastapi import APIRouter, Request

from app.schema.main import CountryNotification
from app.utils.exceptions import BadRequest
from app.utils.response import Response
from app.services.email import email_service

router = APIRouter()


@router.post("/country-added")
async def notify_country_added(request: Request, body: CountryNotification):
    """Endpoint to receive country added notifications."""
    try:
        email_service.send_country_added_notification(body.model_dump())
        return Response(message="Notification sent to admins", status=200)
    except Exception as e:
        raise BadRequest(detail=str(e))
