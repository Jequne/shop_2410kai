from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        login_value = kwargs.get(User.USERNAME_FIELD) or username
        if login_value is None or password is None:
            return None

        user = User.objects.filter(email__iexact=login_value).first()
        if user is None:
            user = User.objects.filter(username__iexact=login_value).first()

        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None