from ..celery import app
from typing import Union
from src.biz.services.mail.sender import MailService


@app.task
def send_on_email(to_email: str, subject: str, body: Union[list, str]):
    MailService.send(
        to=to_email,
        subject=subject,
        contents=[body] if isinstance(body, str) else body
    )
    return "Success send on email"
