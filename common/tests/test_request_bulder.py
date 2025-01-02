from unittest.mock import Mock, patch

import httpx
import pytest

from common.utils.api_client.exceptions import ApiClientException
from conftest import request_builder


class TestRequestBuilder:

    def test_build_url(self,request_builder):
        url = request_builder._build_url('endpoint')
        assert url == "https://api.example.com/endpoint"

    def test_send_post_request_success(self,request_builder):
        builder = request_builder

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"success": True}

        with patch('httpx.Client.post', return_value=mock_response):
            response = builder.send_post_request("endpoint", {"key": "value"})
            assert response.json() == {"success": True}

    def test_send_post_request_timeout(self,request_builder):
        builder = request_builder

        with patch('httpx.Client.post', side_effect=httpx.TimeoutException("Timeout")):
            with pytest.raises(ApiClientException) as exc_info:
                builder.send_post_request("endpoint", {"key": "value"})
            assert exc_info.value.error_code == "TIMEOUT"

    def test_send_post_request_request_error(self,request_builder):
        builder = request_builder

        with patch('httpx.Client.post', side_effect=httpx.RequestError("Request Error")):
            with pytest.raises(ApiClientException) as exc_info:
                builder.send_post_request("endpoint", {"key": "value"})
            assert exc_info.value.error_code == "REQUEST_ERROR"

    def test_send_post_request_http_status_error(self,request_builder):
        builder = request_builder

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found",
                    request=Mock(),
                    response=mock_response
        )

        with patch('httpx.Client.post', return_value=mock_response):
            with pytest.raises(ApiClientException) as exc_info:
                builder.send_post_request("endpoint", {"key": "value"})
            assert exc_info.value.error_code == 404
