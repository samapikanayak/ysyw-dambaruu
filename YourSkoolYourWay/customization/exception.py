from rest_framework.views import exception_handler


def my_custom_exception(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    exec_class = exc.__class__.__name__
    customized_response = {}
    customized_response['status'] = "failed"
    customized_response['errors'] = []
    customized_response['data'] = None

    if response is not None:
        if exec_class ==  "ValidationError":
            for key, value in response.data.items():
                list_to_str = ""
                error = {'field': key, 'message': list_to_str.join(value)}
                customized_response['errors'].append(error)
        elif exec_class == "PermissionDenied":
            for key, value in response.data.items():
                list_to_str = ""
                error = {'field': "permission", 'message': list_to_str.join(value)}
                customized_response['errors'].append(error)
        elif exec_class == "NotAuthenticated":
            for _, value in response.data.items():
                list_to_str = ""
                error = {'field': "authorization", 'message': list_to_str.join(value)}
                customized_response['errors'].append(error)
        elif exec_class == "AuthenticationFailed":
            for key, value in response.data.items():
                list_to_str = ""
                error = {'field': 'authentication', 'message': list_to_str.join(value)}
                customized_response['errors'].append(error)
        elif exec_class == "NotFound":
            for key, value in response.data.items():
                error = {'field': key, 'message': value}
                customized_response['errors'].append(error)

        response.data = customized_response
    return response
