from rest_framework.response import Response as DRFResponse


# Custom Response class.
class InvalidResponse(Exception):
    pass


class Response:
    def __new__(cls, data=None, errors=None, *args, **kwargs):
        payload = cls.format(data, errors)
        return DRFResponse(payload, *args, **kwargs)

    @classmethod
    def format(cls, data, errors):
        data, errors = cls.validate(data, errors)

        message = 'success' if data and not errors else 'failure'

        if not data and not errors:
            raise InvalidResponse('Both data and errors cannot be None')

        return dict(message=message, data=data, errors=errors)

    @classmethod
    def validate(cls, data, errors):
        try:
            data = None if data is None else dict(data)
            errors = None if errors is None else dict(errors)
            return (data, errors)
        except Exception:
            raise InvalidResponse(
                'None or dict-like structure expected for both data and errors')
