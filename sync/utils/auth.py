from django.contrib.auth.backends import ModelBackend
from rental.models.user import MainUser
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
