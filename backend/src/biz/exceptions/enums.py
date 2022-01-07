from src.biz.exceptions.utils import classproperty


class ExceptionEnum:
    """
    Перечисление текста исключений
    """
    # Auth exceptions
    @classproperty
    def account_email_already_exists(cls):
        return "Аккаунт с таким email уже существует"

    @classproperty
    def password_not_equal(cls):
        return "Пароли не равны"

    @classproperty
    def length_password_lt(cls):
        return "Длина пароля должна быть больше 8 символов"

    @classproperty
    def incorrect_auth_data(cls):
        return "Некорректные учетные данные"

    @classproperty
    def authentication_credentials_is_not_valid(cls):
        return "Учетные данные для аутентификации недействительны"

    @classproperty
    def account_by_id_not_found(cls):
        return "Аккаунт с таким id не найден"

    @classproperty
    def account_already_confirmed(cls):
        return "Аккаунт уже подтвержден"

    @classproperty
    def account_by_email_not_found(cls):
        return "Аккаунт с таким email не найден"

    @classproperty
    def account_not_confirmed(cls):
        return "Аккаунт не подтвержден"

    @classproperty
    def email_address_already_use(cls):
        return "Адрес электронной почты уже используется"

    #  city
    @classproperty
    def cities_not_found(cls):
        return "Города не найдены"

    #  examples
    @classproperty
    def maps_examples_not_found(cls):
        return "Примеры не найдены"

    #  maps
    @classproperty
    def maps_not_found(cls):
        return "Доступные платформы карт не найдены"

    #  parser
    @classproperty
    def type_parser_not_found(cls):
        return "Тип парсера не найден"

    #  order
    @classproperty
    def order_not_found(cls):
        return "Заказ не найден"
