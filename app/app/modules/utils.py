import base64
import logging
import secrets
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils.crypto import get_random_string
from customer.models import *


def log_request(*args):
    for arg in args:
        logging.info(arg)


def encrypt_text(text: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
    fernet = Fernet(key)
    secure = fernet.encrypt(f"{text}".encode())
    return secure.decode()


def decrypt_text(text: str):
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32])
    fernet = Fernet(key)
    decrypt = fernet.decrypt(text.encode())
    return decrypt.decode()


def generate_random_password():
    return get_random_string(length=10)


def generate_random_otp():
    return get_random_string(length=6, allowed_chars="1234567890")

def incoming_request_checks(request, require_data_field: bool = True) -> tuple:
    try:
        x_api_key = request.headers.get("X-Api-Key", None) or request.META.get(
            "HTTP_X_API_KEY", None
        )
        request_type = request.data.get("requestType", None)
        data = request.data.get("data", {})

        if not x_api_key:
            return False, "Missing or Incorrect Request-Header field 'X-Api-Key'"

        if x_api_key != settings.X_API_KEY:
            return False, "Invalid value for Request-Header field 'X-Api-Key'"

        if not request_type:
            return False, "'requestType' field is required"

        if request_type != "inbound":
            return False, "Invalid 'requestType' value"

        if require_data_field:
            if not data:
                return (
                    False,
                    "'data' field was not passed or is empty. It is required to contain all request data",
                )

        return True, data
    except (Exception,) as err:
        return False, f"{err}"


def get_incoming_request_checks(request) -> tuple:
    try:
        x_api_key = request.headers.get("X-Api-Key", None) or request.META.get(
            "HTTP_X_API_KEY", None
        )

        if not x_api_key:
            return False, "Missing or Incorrect Request-Header field 'X-Api-Key'"

        if x_api_key != settings.X_API_KEY:
            return False, "Invalid value for Request-Header field 'X-Api-Key'"

        return True, ""

    except (Exception,) as err:
        return False, f"{err}"


def api_response(message, status: bool, data=None, **kwargs) -> dict:
    if data is None:
        data = {}
    try:
        reference_id = secrets.token_hex(30)
        response = dict(
            requestTime=timezone.now(),
            requestType="outbound",
            referenceId=reference_id,
            status=status,
            message=message,
            data=data,
            **kwargs,
        )

        # if "accessToken" in data and 'refreshToken' in data:
        if "accessToken" in data:
            # Encrypting tokens to be
            response["data"]["accessToken"] = encrypt_text(text=data["accessToken"])
            # response['data']['refreshToken'] = encrypt_text(text=data['refreshToken'])
            logging.info(msg=response)

            response["data"]["accessToken"] = decrypt_text(text=data["accessToken"])
            # response['data']['refreshToken'] = encrypt_text(text=data['refreshToken'])

        else:
            logging.info(msg=response)

        return response
    except (Exception,) as err:
        return err


def customPagination(request, data, count):
    page = int(request.GET.get("page", "1"))
    next = page + 1
    prev = page - 1
    page = page * 50
    start_page = page - 50
    if count > 10000:
        count = 10000
    result = {
        "next": next,
        "previous": prev,
        "count": count,
        "results": data,
    }
    return result
