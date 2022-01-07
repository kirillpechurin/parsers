import datetime
import hashlib
from typing import Optional, Union

import pytz
from bson import ObjectId
from pydantic import EmailStr

from app.models.auth import Account
from src.biz.exceptions.custom import InternalError, ValidationError
from src.biz.services.base_service import BaseService

from src.biz.exceptions.enums import ExceptionEnum
from src.cel.tasks.send_mail import send_on_email


class AuthService(BaseService):

    def __init__(self):
        super(AuthService, self).__init__()
        self.collection = self.db_name['account']

    @staticmethod
    def create_hash_password(password: str) -> Optional[hashlib.sha512]:
        """
        Генерирует простой хешированный пароль

        :param password: исходный пароль
        :return: хешированный пароль или raise error
        """
        try:
            hash_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        except:
            raise InternalError(message="Ошибка шифрования пароля")
        return hash_password

    def check_on_email(self, email: EmailStr) -> Optional[bool]:
        """
        Проверка, существует ли такой email

        :param email: исходный email
        :return: True - если существует, False - если нет
        """
        result = self.collection.find_one({"email": email})
        if result:
            return True
        return False

    @staticmethod
    def check_password(password: str, repeat_password: str) -> None:
        """
        Проверка пароля на валидность.

        Вызывает исключения в случае невалидности пароля

        :param password: исходный пароль
        :param repeat_password: повторный исходный пароль
        :return: None
        """
        if password != repeat_password:
            raise ValidationError(ExceptionEnum.password_not_equal)
        elif len(password) < 8:
            raise ValidationError(ExceptionEnum.length_password_lt)

    @staticmethod
    def send_confirmation_link(account_id: str, email: EmailStr, origin_server: str) -> None:
        """
        Отправляет письмо с подтверждением на email

        Генерирует ссылку и отправляет ее
        :param account_id: id аккаунта
        :param email: email аккаунта
        :param origin_server: Клиент
        :return: None
        """
        link = f"{origin_server}/confirm_email/{account_id}"
        subject = "Подтверждение аккаунта"
        body = f"""Перейдите по ссылке для подтверждения. <a href="{link}">Подтвердить аккаунт</a>"""
        send_on_email.delay(email, subject, body)

    def create_account(self, email: EmailStr, password: str, repeat_password: str, origin_server: str) -> Optional[Account]:
        """
        Создание аккаунта

        Сначала проверяет на существование email, потом проверка валидности пароля и наконец сохранение сущности

        :param email: email
        :param password: исходный пароль
        :param repeat_password: повторение исходного пароля
        :param origin_server: Клиент
        :return: Account
        """
        exists = self.check_on_email(email)
        if exists:
            raise ValidationError(ExceptionEnum.account_email_already_exists)

        self.check_password(password, repeat_password)
        created_at = datetime.datetime.now(tz=pytz.UTC)
        new_account = self.collection.insert_one({
            "first_name": "",
            "last_name": "",
            "confirmed": False,
            "email": email,
            "password": self.create_hash_password(password),
            "created_at": created_at
        })
        account_id = str(new_account.inserted_id)
        self.send_confirmation_link(account_id, email, origin_server)
        return Account.parse_obj({"account_id": account_id,
                                  "email": email,
                                  "created_at": created_at})

    def check_by_auth_data(self, email: Union[EmailStr, str], password: str) -> Optional[Account]:
        """
        Проверка по данным аутентификации

        :param email: email
        :param password: исходный пароль
        :return: Account or raise Error
        """
        account = self.collection.find_one({"email": email, "password": self.create_hash_password(password)})
        if not account:
            raise ValidationError(ExceptionEnum.incorrect_auth_data)
        return Account.parse_obj(account)

    def get_account(self, email: EmailStr, password: str) -> Account:
        """
        Получить аккаунт

        :param email: email
        :param password: исходный пароль
        :return: Account
        """
        account = self.check_by_auth_data(email, password)
        return account

    def get_by_id(self, account_id: str) -> Optional[Account]:
        """
        Получить аккаунт по id

        :param account_id: string id аккаунта
        :return: Account or raise Error
        """
        obj_account = self.collection.find_one({"_id": ObjectId(account_id)})
        if not obj_account:
            raise ValidationError(ExceptionEnum.account_by_id_not_found)
        return Account.parse_obj(obj_account)

    def confirm_account(self, account_id: str) -> None:
        """
        Подтвердить аккаунт по id

        :param account_id: string id аккаунта
        :return: None
        """
        self.collection.update_one({"_id": ObjectId(account_id)}, {"$set": {"confirmed": True}})

    def get_by_email(self, email: EmailStr) -> Optional[Account]:
        """
        Получить аккаунт по email

        :param email: email аккаунта
        :return: Account or raise Error
        """
        obj_account = self.collection.find_one({"email": email})
        if not obj_account:
            raise ValidationError(ExceptionEnum.account_by_email_not_found)
        return Account.parse_obj(obj_account)

    @staticmethod
    def send_forgot_link(account_id: str, email: EmailStr, origin_server: str) -> None:
        """
        Отправить ссылку на восстановление пароля

        :param account_id: string id аккаунта
        :param email: email аккаунта
        :param origin_server: Клиент
        :return: None
        """
        link = f"{origin_server}/reset_password/{account_id}"
        subject = "Восстановление пароля"
        body = f"""Перейдите по ссылке для сброса пароля. \n\n <a href="{link}">Сбросить пароль</a>"""
        send_on_email.delay(email, subject, body)

    def update_password(self, account_id: str, password: str, repeat_password: str) -> None:
        """
        Обновить пароль

        Проверка, что пароль валиден и обновление пароля
        :param account_id: string id аккаунта
        :param password: исходный пароль
        :param repeat_password: Повторный исходный пароль
        :return:
        """
        self.check_password(password, repeat_password)
        self.collection.update_one(
            {
                "_id": ObjectId(account_id)
            },
            {
                "$set": {"password": self.create_hash_password(password)}
            }
        )

    def update_email(self, account_id: str, email: EmailStr) -> None:
        """
        Обновить email

        Проверка, что email не занят
        Сохранение с неподтверждением
        Отправка ссылки для подтверждения аккаунта

        :param account_id: string id аккаунта
        :param email: новый email
        :return: None
        """
        if self.check_on_email(email):
            raise ValidationError(ExceptionEnum.email_address_already_use)
        self.collection.update_one({"_id": ObjectId(account_id)},
                                   {"$set": {"email": email,
                                             "confirmed": False}})
        self.send_confirmation_link(account_id, email)

    def update_account_info(self, account_id: str, first_name: str, last_name: str) -> None:
        """
        Обновить информацию об аккаунте

        Частично обновляет информацию

        :param account_id: string id аккаунта
        :param first_name: Имя
        :param last_name: Фамилия
        :return: None
        """
        if not isinstance(first_name, str) and not isinstance(last_name, str):
            return None

        self.collection.update_one(
            {"_id": ObjectId(account_id)},
            {
                "$set": {
                    "first_name": first_name,
                    "last_name": last_name
                } if isinstance(first_name, str) and isinstance(last_name, str) else {
                    "first_name": first_name
                } if isinstance(first_name, str) else {
                    "last_name": last_name
                }
            }
        )
