import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from fastapi.templating import Jinja2Templates

from src.config import smtp_settings

templates = Jinja2Templates(directory='src/templates')


def send_email(
    template_name: str, receiver: str, subject: str, data: dict[str, Any]
) -> None:
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = smtp_settings.SENDER
    message['To'] = receiver
    template = templates.get_template(template_name)
    email_html = template.render(subject=subject, **data)
    part = MIMEText(email_html, 'html')
    message.attach(part)

    with smtplib.SMTP_SSL(
        smtp_settings.SMTP_SERVER, smtp_settings.PORT
    ) as server:
        server.set_debuglevel(1)
        server.login(smtp_settings.LOGIN, smtp_settings.PASSWORD)
        server.sendmail(smtp_settings.SENDER, receiver, message.as_string())
