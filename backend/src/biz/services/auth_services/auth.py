import datetime
import hashlib
from typing import Optional, Union

import pytz
from bson import ObjectId
from pydantic import EmailStr

from app.models.auth import Account
from src.biz.exceptions.custom import InternalError, ValidationError
from src.biz.services.base_service import BaseService
from src.biz.services.mail.sender import MailService


class AuthService(BaseService):

    def __init__(self):
        super(AuthService, self).__init__()
        self.collection = self.db_name['account']

    @staticmethod
    def create_hash_password(password: str) -> Optional[hashlib.sha512]:
        try:
            hash_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        except:
            raise InternalError
        return hash_password

    def check_on_email(self, email: EmailStr) -> Optional[bool]:
        result = self.collection.find_one({"email": email})
        if result:
            return True
        return False

    @staticmethod
    def check_password(password: str, repeat_password: str) -> None:
        if password != repeat_password:
            raise ValidationError("Passwords does not equal")
        elif len(password) < 8:
            raise ValidationError("Length password might be more than 8")

    @staticmethod
    def send_confirmation_link(account_id: str, email: EmailStr) -> None:
        link = f"http://url/{account_id}"
        MailService().send(to=email,
                           subject="Confirm account",
                           contents=[f"Перейдите по ссылке для подтверждения. \n\n {link}"]
                           )

    def create_account(self, email: EmailStr, password: str, repeat_password: str) -> Optional[Account]:
        exists = self.check_on_email(email)
        if exists:
            raise ValidationError("Account with this email already exists")

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
        self.send_confirmation_link(account_id, email)
        return Account.parse_obj({"account_id": account_id,
                                  "email": email,
                                  "created_at": created_at})

    def check_by_auth_data(self, email: Union[EmailStr, str], password: str) -> Optional[Account]:
        account = self.collection.find_one({"email": email, "password": self.create_hash_password(password)})
        if not account:
            raise ValidationError("Incorrect auth data")
        return Account.parse_obj(account)

    def get_account(self, email: EmailStr, password: str) -> Account:
        account = self.check_by_auth_data(email, password)
        return account

    def get_by_id(self, account_id: str) -> Optional[Account]:
        obj_account = self.collection.find_one({"_id": ObjectId(account_id)})
        if not obj_account:
            raise ValidationError("Account with such id was not found")
        return Account.parse_obj(obj_account)

    def confirm_account(self, account_id: str) -> None:
        self.collection.update_one({"_id": ObjectId(account_id)}, {"$set": {"confirmed": True}})

    def get_by_email(self, email: EmailStr) -> Optional[Account]:
        obj_account = self.collection.find_one({"email": email})
        if not obj_account:
            raise ValidationError("Account with such email was not found")
        return Account.parse_obj(obj_account)

    @staticmethod
    def send_forgot_link(account_id: str, email: EmailStr) -> None:
        link = f"http://url/{account_id}"
        MailService().send(
            to=email,
            subject="Reset password link",
            contents=[f"Перейдите по ссылке для сброса пароля.\n\n {link}"]
        )

    def update_password(self, account_id: str, password: str, repeat_password: str) -> None:
        self.check_password(password, repeat_password)
        self.collection.update_one(
            {
                "_id": ObjectId(account_id)
            },
            {
                "$set": {"password": self.create_hash_password(password)}
            }
        )
