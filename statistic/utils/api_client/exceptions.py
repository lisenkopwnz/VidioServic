import logging

logger = logging.getLogger('recommendation_system_errors')

class ErrorTranslatorDescriptor:
    """
    Дескриптор, преобразующий низкоуровневые ошибки в высокоуровневые сообщения, понятные клиентам.
    Перед преобразованием выполняется логирование исходных ошибок для технического анализа.
    """

    def __init__(self, message: str):
        self.message = message

    def __get__(self, instance, owner):
        """Возвращаем текущее значение атрибута."""
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value: str):
        """Логируем ошибку и заменяем сообщение на понятное клиенту."""
        logging.error(f'Произошла ошибка: {value}')
        instance.__dict__[self.name]=self.message

    def __set_name__(self, owner, name):
        """Сохраняем имя атрибута при связывании дескриптора."""
        self.name = name

class ApiClientException(Exception):
    """
        Исключение для API клиента, которое используется для обработки ошибок
        и преобразования их в высокоуровневые сообщения для клиентов.
    """
    message = ErrorTranslatorDescriptor("Неудалось загрузить рекомендации")

    def __init__(self, message: str, error_code: int = None):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
