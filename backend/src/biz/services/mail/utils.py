import os

import yagmail


def get_connection() -> yagmail.SMTP:
    return yagmail.SMTP(os.environ.get("MAIL_SENDER_NAME"), os.environ.get("MAIL_SENDER_PASSWORD"))
