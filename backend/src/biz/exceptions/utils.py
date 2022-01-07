class classproperty(object):
    """
    класс-декоратор для обращения к методам как к свойствам

    Не требует экземлпяра класса
    Взаимодействует через сам класс (cls)
    """
    def __init__(self, f):
        """
        Добавляем функцию в атрибут класса
        :param f: функция, которую мы оборачиваем
        """
        self.f = f

    def __get__(self, obj, owner):
        """
        :param obj: pass
        :param owner: cls
        :return: результат работы функции
        """
        return self.f(owner)
