from django.db import models

class UserProfile(models.Model):
    email = models.TextField(unique=True)
    password = models.TextField(max_length=100)
    user_vector = models.JSONField()
    swiped_items = models.JSONField(default=list)

class ClothItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=200)
    colors_available = models.TextField()
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
