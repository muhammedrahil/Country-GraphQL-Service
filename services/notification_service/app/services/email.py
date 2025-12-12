import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import settings


class EmailNotificationService:
    """Service to send email notifications."""

    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.from_email
        self.admin_email = settings.admin_email

    def send_country_added_notification(self, country_data: dict):
        """Send email notification when a new country is added."""
        subject = f"New Country Added: {country_data.get('name')}"

        html_body = f"""
        
        
            New Country Added to Database

                FieldValue
                Name{country_data.get('name')}
                Code{country_data.get('alpha2_code')}
                Capital{country_data.get('capital')}
                Region{country_data.get('region')}
                Population{country_data.get('population'):,}
                Added At{country_data.get('created_at')}



        """

        self._send_email(self.admin_email, subject, html_body)

    def _send_email(self, to_email: str, subject: str, html_body: str):
        """Send an email."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email

            html_part = MIMEText(html_body, "html")
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")


email_service = EmailNotificationService()
