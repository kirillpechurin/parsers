from typing import List

from .utils import get_connection


class MailService:

    @staticmethod
    def send(to: str,
             subject: str,
             contents: List[str]
             ) -> None:
        """
        Отправить сообщение

        :param to: Получатель
        :param subject: Заголовок
        :param contents: Контент - список
        :return: None
        """
        try:
            connection = get_connection()
            connection.send(
                to=to,
                subject=subject,
                contents=contents
            )
        except Exception:
            pass
