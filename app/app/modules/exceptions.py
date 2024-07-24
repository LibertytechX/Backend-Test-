import datetime
import secrets
from rest_framework.exceptions import APIException
from .utils import log_request


class InvalidRequestException(APIException):
    status_code = 400
    default_detail = "Invalid request"
    default_code = "invalid_request"


def raise_serializer_error_msg(errors: dict):
    data = dict()
    data["requestTime"] = str(datetime.datetime.now())
    data["requestType"] = "outbound"
    data["referenceId"] = secrets.token_hex(30)
    data["status"] = False
    for err_key, err_val in errors.items():
        if type(err_val) is list:
            err_msg = ", ".join(err_val)
            msg = f'Error occurred on \'{err_key.replace("_", " ")}\' field: {err_msg}'
            data["message"] = msg
        else:
            for err_val_key, err_val_val in err_val.items():
                err_msg = ", ".join(err_val_val)
                msg = f"Error occurred on '{err_val_key}' field: {err_msg}"
                # msg = f'Error occurred on \'{err_val_key.replace("_", " ")}\' field: {err_msg}'
                data["message"] = msg
        log_request(data)
        raise InvalidRequestException(data)


def create_error_message(key, values):
    data = dict()
    data[key] = str(values).split("|")
    raise InvalidRequestException({"message": values})
