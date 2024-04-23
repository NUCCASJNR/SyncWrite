from django.contrib.auth.backends import ModelBackend
from sync.models.user import MainUser
from django.core.exceptions import ObjectDoesNotExist


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = MainUser.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None

    def authenticate_header(self, request):
        return 'Bearer realm="api"'


def get_client_ip(request):
    """
    Retrieves the client's IP address from the request.

    This function attempts to extract the client's IP address from the HTTP headers.
    If the 'HTTP_X_FORWARDED_FOR' header is present, it contains a comma-separated list
    of IP addresses, with the client's IP address typically being the first one.
    If the 'HTTP_X_FORWARDED_FOR' header is not present, the 'REMOTE_ADDR' header is used
    to obtain the client's IP address.

    Args:
        request: HttpRequest object representing the incoming HTTP request.

    Returns:
        str: The client's IP address.

    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0].strip()
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip
