from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import generics, permissions
from .models import User, Role
from .serializers import UserMinimalSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserProfileSerializer


class MasterListView(generics.ListAPIView):
    """Эндпоинт для получения списка всех мастеров (доступен только админам)"""

    serializer_class = UserMinimalSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(role=Role.MASTER)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Отдает профиль текущего запрашивающего пользователя
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
