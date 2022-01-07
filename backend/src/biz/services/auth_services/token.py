import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
import pytz

from src.biz.exceptions.custom import ValidationError, InternalError

from src.biz.exceptions.enums import ExceptionEnum

OBJECT_UTC = pytz.UTC


DATE_EXPRESSION = "%Y-%m-%d %H:%M:%S"
TOKEN_LIFETIME_SECONDS = 60 * 60 * 24
SECRET_KEY_TOKEN = os.environ.get("SECRET_KEY_TOKEN")
ALGORITHM = os.environ.get("ALGORITHM_TOKEN")


def get_now() -> datetime:
    """
    Получить время сейчас
    :return: datetime.datetime object
    """
    return datetime.now(tz=OBJECT_UTC)


def compare_date_gt_str_date(date: datetime, str_date: str) -> bool:
    """
    Сравнить что дата больше, чем строка даты

    Первый аргумент
    :param date: datetime объект
    :param str_date: str объект даты
    :return: True - если первый аргумент больше второго, False - если первый аргумент меньше второго
    """
    date_str_date = datetime.strptime(str_date, DATE_EXPRESSION)
    if date > OBJECT_UTC.localize(date_str_date):
        return True
    return False


def get_str_date(date: datetime) -> str:
    """
    Получить строку из даты по форматированию

    :param date: дата
    :return: str дата
    """
    return date.strftime(DATE_EXPRESSION)


class JWTService:

    @staticmethod
    def create_token(account_id: str) -> Optional[jwt]:
        """
        Создание json web token

        :param account_id: id аккаунта
        :return: jwt
        """
        try:
            str_delta = get_str_date(datetime.now(tz=pytz.UTC) + timedelta(seconds=TOKEN_LIFETIME_SECONDS))
            return jwt.encode(
                {
                    "account_id": account_id,
                    "expires_in": str_delta
                },
                SECRET_KEY_TOKEN,
                algorithm=ALGORITHM
            )
        except:
            raise InternalError

    @staticmethod
    def decode_token(value: str) -> str:
        """
        Декодирование токена

        :param value: предпологаемый токен
        :return: id аккаунта
        """
        try:
            payload = jwt.decode(value, key=SECRET_KEY_TOKEN, algorithms=[ALGORITHM])

            expires_in = payload['expires_in']
            now_datetime = get_now()
            if compare_date_gt_str_date(now_datetime, expires_in):
                raise ValidationError

            return payload['account_id']
        except Exception:
            raise ValidationError(ExceptionEnum.authentication_credentials_is_not_valid)
