import os
from typing import List

import yagmail

from src.biz.exceptions.custom import InternalError


class MailService:

    def get_connection(self) -> yagmail.SMTP:
        """
        Получить соединение по smtp

        :return: yagmail.SMTP
        """
        return yagmail.SMTP(os.environ.get("MAIL_SENDER_NAME"), os.environ.get("MAIL_SENDER_PASSWORD"))

    def send(self,
             to: str,
             subject: str,
             contents: List[str]
             ):
        """
        Отправить сообщение

        :param to: Получатель
        :param subject: Заголовок
        :param contents: Контент - список
        :return: None
        """
        try:
            connection = self.get_connection()
            connection.send(
                to=to,
                subject=subject,
                contents=contents
            )
        except Exception:
            raise InternalError
