from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import EmployeeProfile, ResidentProfile, User


class UserMinimalSerializer(serializers.ModelSerializer):
    position = serializers.CharField(
        source="employee_profile.position", read_only=True, default="Мастер"
    )

    class Meta:
        model = User
        fields = ["id", "username", "full_name", "role", "position"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["role"] = user.role
        token["full_name"] = user.full_name or user.username
        token["username"] = user.username

        return token


class ResidentProfileSerializer(serializers.ModelSerializer):
    apartment_number = serializers.CharField(source="apartment.number", read_only=True)
    building_address = serializers.CharField(
        source="apartment.building.address", read_only=True
    )

    class Meta:
        model = ResidentProfile
        fields = ["building_address", "apartment_number"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ["position", "department", "is_active_worker"]


class UserProfileSerializer(serializers.ModelSerializer):
    resident_profile = ResidentProfileSerializer(read_only=True)
    employee_profile = EmployeeProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "phone",
            "role",
            "resident_profile",
            "employee_profile",
        ]
