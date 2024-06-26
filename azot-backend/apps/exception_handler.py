from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    try:
        exception_class = exc.__class__.__name__
        handlers = {
            'IntegrityError': _handler_integrity_error,
            'ValidationError': _handler_validation_error,
            'DoesNotExist': _handler_not_found,
            'PurchaseError': _handler_purchase_error,
            'PermissionDenied': _handler_permission_denied,
            'NotActivated': _handler_not_activated,
            'WrongPasswordError': _handler_wrong_password_error,
            # Add more handlers as needed
        }
        res = exception_handler(exc, context)

        if exception_class in handlers:
            # calling hanlder based on the custom
            message, status_code = handlers[exception_class](exc, context, res)
        else:
            # if there is no hanlder is presnet
            message = str(exc)
            status_code = HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data={'error': message}, status=status_code)
    except Exception as e:
        return Response(data={'error': 'Internal server error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


def _handler_validation_error(exc, context, res):
    return "Invalid data", 400


def _handler_integrity_error(exc, context, res):
    if 'Client' in context['view'].__class__.__name__:
        return "Client already exists", 400
    elif 'Seller' in context['view'].__class__.__name__:
        return "Seller already exists", 400
    else:
        return "Integrity error", 400


def _handler_not_found(exc, context, res):
    if 'Login' in context['view'].__class__.__name__:
        return "Wrong email or password", 400
    else:
        return str(exc), 400



def _handler_purchase_error(exc, context, res):
    return exc.detail, 400


def _handler_permission_denied(exc, context, res):
    return exc.detail, 400

def _handler_not_activated(exc, context, res):
    return exc.detail, 400


def _handler_wrong_password_error(exc, context, res):
    return exc.detail, 400