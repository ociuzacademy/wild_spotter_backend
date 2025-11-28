from django.db import models


class TblRegister(models.Model):
    """Model for user registration."""
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=190, unique=True)
    password = models.CharField(max_length=100)  # plain text for demo (use hashing in production)
    role=models.CharField(max_length=100,default='user')
    class Meta:
        db_table = 'tbl_register'
        verbose_name = 'User Registration'
        verbose_name_plural = 'User Registrations'
        ordering = ['username']

    def __str__(self):
        return self.username



from django.db import models
# from userapp.models import tbl_register
from adminapp.models import Topic

class Journal(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("Published", "Published"),
        ("rejected","Rejected")
    ]

    user = models.ForeignKey(TblRegister, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "journal"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

from adminapp.models import *
from django.db.models import Avg
class RecentSighting(models.Model):
    user = models.ForeignKey(TblRegister, on_delete=models.CASCADE, related_name="sightings")
    sanctuary = models.ForeignKey(TblWildLifeSanctuary, on_delete=models.CASCADE, related_name="sightings")

    species = models.CharField(max_length=200)
    Scientific_name = models.CharField(max_length=200)

    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="sightings_images/", blank=True, null=True)
    video = models.FileField(upload_to="sightings_videos/", blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "recent_sightings"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.species} - {self.user.username}"

    @property
    def average_rating(self):
        return self.ratings.aggregate(Avg("rating"))["rating__avg"]

# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from wildspotter_api.models import TblRegister
from .models import RecentSighting

class SightingRating(models.Model):
    user = models.ForeignKey(
        TblRegister,
        on_delete=models.CASCADE,
        related_name="sighting_ratings"
    )
    sighting = models.ForeignKey(
        RecentSighting,
        on_delete=models.CASCADE,
        related_name="ratings"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sighting_ratings"
        unique_together = ("user", "sighting")   # prevents duplicate ratings
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.rating}★"
