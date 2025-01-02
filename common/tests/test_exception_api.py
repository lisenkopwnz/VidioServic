from common.utils.api_client.exceptions import ApiClientException


class TestApiClientException:
    def test_exception_initialization(self):
        """
        Проверяем, что исключение корректно инициализируется.
        """
        exception = ApiClientException("Ошибка сервера", error_code=500)

        # Проверяем, что сообщение и код ошибки установлены
        assert str(exception) == "Ошибка сервера"
        assert exception.error_code == 500

    def test_descriptor_replaces_message(self):
        """
        Проверяем, что дескриптор заменяет сообщение в исключении.
        """
        exception = ApiClientException("Низкоуровневая ошибка")

        # Проверяем, что сообщение было заменено дескриптором
        assert exception.message == "Неудалось загрузить рекомендации"