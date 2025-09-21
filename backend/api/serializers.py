from rest_framework import serializers
from .models import ClothItem, Waitlist, UserProfile
from django.contrib.auth.hashers import make_password

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "email", "password", "user_vector", "swiped_items"]
        extra_kwargs = {
            "password": {"write_only": True},
            "user_vector": {"required": False},   # not required from client
            "swiped_items": {"required": False}   # not required from client
        }

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["user_vector"] = [0] * 2049
        validated_data["swiped_items"] = []
        return UserProfile.objects.create(**validated_data)

class ClothItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothItem
        fields = '__all__'

class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = '__all__'
