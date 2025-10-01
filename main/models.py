import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    CATEGORY_CHOICES = [
    ("jersey", "Jerseys"),
    ("shorts", "Shorts"),
    ("shoes", "Football Boots"),
    ("socks", "Socks"),
    ("ball", "Football"),
    ("goalkeeper", "Goalkeeper Gear"),
    ("training", "Training Equipment"),
    ("bag", "Bags"),
    ("accessories", "Accessories"),
    ("fan_merch", "Fan Merchandise"),
]
    
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(choices=CATEGORY_CHOICES, default='jersey')
    is_featured = models.BooleanField()