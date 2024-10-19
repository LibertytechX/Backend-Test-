from rest_framework.response import Response


def service_response(
    status: str = "success", data: dict = {}, message: str = "", status_code=200
) -> Response:
    """Api response utils functions

    Args:
        status (str, optional): request status Defaults to "success".
        data (dict, optional): response data. Defaults to None.
        message (str, optional): response message. Defaults to None.
        status (int, optional): response status code. Defaults to 200.

    Returns:
        Response: Http response
    """
    return Response(
        {"status": status, "message": message, "data": data}, status=status_code
    )
