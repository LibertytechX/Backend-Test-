from utils.responses import success_response


class SuccessResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code < 400:
            response = success_response(
                data=response.data,
                message=getattr(self, 'success_message', 'Success'),
                status_code=response.status_code
            )
        return super().finalize_response(request, response, *args, **kwargs)
