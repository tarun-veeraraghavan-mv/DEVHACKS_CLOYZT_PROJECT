from rest_framework import serializers
from .models import ClothItem

class ClothItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothItem
        fields = '__all__'
