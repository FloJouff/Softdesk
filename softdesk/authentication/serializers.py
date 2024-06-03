from django.core.exceptions import ValidationError
from rest_framework import serializers
from authentication.models import User
from datetime import date


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "date_of_birth", "can_be_contacted", "can_data_be_shared"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            date_of_birth=validated_data["date_of_birth"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        return user

    def validate_date_of_birth(self, value):
        """Check if user is old enought to create a profil"""
        today = date.today()
        min_age = 15
        min_birth_date = today.replace(year=today.year - min_age)

        if value > min_birth_date:
            raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire")
        return value
