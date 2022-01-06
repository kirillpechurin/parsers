import os

import yagmail


class MailService:

    def get_connection(self):
        return yagmail.SMTP(os.environ.get("MAIL_SENDER_NAME"), os.environ.get("MAIL_SENDER_PASSWORD"))

    def send(self,
             to,
             subject,
             contents
             ):
        connection = self.get_connection()
        connection.send(
            to=to,
            subject=subject,
            contents=contents
        )
