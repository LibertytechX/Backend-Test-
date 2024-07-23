from rest_framework.exceptions import APIException


class OutOfStocksException(APIException):
    status_code = 404
    default_code = 404
    default_detail = "The requested product is not available at this time."
