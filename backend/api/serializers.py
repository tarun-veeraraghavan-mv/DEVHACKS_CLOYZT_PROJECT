from rest_framework import serializers
from .models import ClothItem, Waitlist

class ClothItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothItem
        fields = '__all__'

class WaitlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waitlist
        fields = '__all__'
