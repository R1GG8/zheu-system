from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Кастомный бэкенд для аутентификации через email или username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # Ищем пользователя по username ИЛИ по email
            user = UserModel.objects.get(Q(username=username) | Q(email=username))
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # На случай, если каким-то чудом нашлось несколько (не должно быть при unique=True)
            return (
                UserModel.objects.filter(Q(username=username) | Q(email=username))
                .order_by("id")
                .first()
            )

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
