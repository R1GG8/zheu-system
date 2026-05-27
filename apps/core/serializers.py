from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем кастомные поля в payload JWT-токена
        token['role'] = user.role
        token['full_name'] = user.full_name or user.username
        token['username'] = user.username

        return token