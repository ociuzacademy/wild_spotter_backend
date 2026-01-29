from django.db import models


class AdminProfile(models.Model):
    """Stores admin login credentials and profile details."""
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=190, unique=True)
    admin_password = models.CharField(max_length=100)
    role=models.CharField(max_length=100,default='admin')

    class Meta:
        db_table = 'admin_profile'
        verbose_name = "Admin Profile"  
        verbose_name_plural = "Admin Profiles"
        ordering = ['name']

    def __str__(self):
        return self.name


class WildAnimalCategory(models.Model):
    """Represents a category of wild animals, like Mammals, Birds, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wild_animal_category'
        verbose_name = 'Wild Animal Category'
        verbose_name_plural = 'Wild Animal Categories'
        ordering = ['name']

    def __str__(self):
        return self.name





from django.db import models


class WildAnimalCategory(models.Model):
    """
    Represents a category of wild animals (e.g., Mammals, Birds, Reptiles).
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wild_animal_category"
        verbose_name = "Wild Animal Category"
        verbose_name_plural = "Wild Animal Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class WildAnimal(models.Model):
    """
    Represents an individual wild animal and its biological and conservation details.
    """

    CONSERVATION_STATUS_CHOICES = [
        ("Least Concern", "Least Concern"),
        ("Near Threatened", "Near Threatened"),
        ("Vulnerable", "Vulnerable"),
        ("Endangered", "Endangered"),
        ("Critically Endangered", "Critically Endangered"),
        ("Extinct in the Wild", "Extinct in the Wild"),
        ("Extinct", "Extinct"),
    ]

    category = models.ForeignKey(
        WildAnimalCategory,
        on_delete=models.CASCADE,
        related_name="animals",
        help_text="Select the animal's biological category.",
    )
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True, null=True)
    habitat = models.TextField(blank=True, null=True)
    diet = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=100, blank=True, null=True)
    lifespan = models.CharField(max_length=100, blank=True, null=True)
    conservation_status = models.CharField(
        max_length=50,
        choices=CONSERVATION_STATUS_CHOICES,
        help_text="Select conservation status according to IUCN Red List.",
    )
    conservation_source = models.CharField(
        max_length=100,
        default="IUCN Red List",
        help_text="Specify the conservation reference source.",
    )
    about = models.TextField(blank=True, null=True)

    # 🖼️ New field for image upload
    image = models.ImageField(
        upload_to="animal_images/",
        blank=True,
        null=True,
        help_text="Upload an image representing the animal.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wild_animal"
        verbose_name = "Wild Animal"
        verbose_name_plural = "Wild Animals"
        ordering = ["name"]

    def __str__(self):
        return self.name





class TblWildLifeSanctuary(models.Model):
    """Model to store details about a wildlife sanctuary."""
    name = models.CharField(max_length=200)
    species_count = models.IntegerField(default=0, null=True, blank=True)

    hectare = models.PositiveIntegerField(help_text="Number of hectares", default=0)
    viewpoints = models.PositiveIntegerField(help_text="Number of viewpoints", default=0)
    visitors_per_month = models.PositiveIntegerField(help_text="Monthly visitors count", default=0)
    about = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wild_life_sanctuary'
        verbose_name = 'Wild Life Sanctuary'
        verbose_name_plural = 'Wild Life Sanctuaries'

    def __str__(self):
        return self.name


class TblSanctuaryImage(models.Model):
    """Model to store multiple images for a sanctuary."""
    sanctuary = models.ForeignKey(TblWildLifeSanctuary, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='wildlife_sanctuary/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sanctuary_images'




from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone
from wildspotter_api.models import TblRegister  # ✅ Import your user model

class Community(models.Model):
    """Model to store communities related to a wildlife sanctuary."""
    name = models.CharField(max_length=200)
    sanctuary = models.ForeignKey('TblWildLifeSanctuary', on_delete=models.CASCADE, related_name='communities')
    picture = models.ImageField(upload_to='community_images/', blank=True, null=True)
    members = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    # 🧠 New Field — Tracks which users joined
    joined_users = models.ManyToManyField(TblRegister, related_name='joined_communities', blank=True)

    class Meta:
        db_table = 'community'
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

    def __str__(self):
        return self.name




class Topic(models.Model):
    """Topics like Birdwatching, Flora, Fauna, Conservation, etc."""
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'topics'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['name']

    def __str__(self):
        return self.name




from django.db import models
from django.utils import timezone
from adminapp.models import TblWildLifeSanctuary

class ForestOfficer(models.Model):
    officer_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    sanctuary = models.ForeignKey(
        TblWildLifeSanctuary,
        on_delete=models.CASCADE,
        related_name="officers",
        null=True,
        blank=True
    )

    profile_image = models.ImageField(upload_to='officers_profile/', blank=True, null=True)
    id_card_image = models.ImageField(upload_to='officers_idcards/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    role=models.CharField(max_length=100,default='forest_officer')
    class Meta:
        db_table = "forest_officers"
        ordering = ['name']

    def __str__(self):
        return self.name





from django.db import models
from adminapp.models import ForestOfficer

class AwarenessPoster(models.Model):
    officer = models.ForeignKey(
        ForestOfficer,
        on_delete=models.CASCADE,
        related_name="posters"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="awareness_posters/")

    category = models.CharField(
        max_length=100,
        choices=[
            ("wildlife_protection", "Wildlife Protection"),
            ("forest_fire", "Forest Fire Awareness"),
            ("anti_poaching", "Anti-Poaching"),
            ("general", "General Awareness"),
        ],
        default="general"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "awareness_posters"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title





from django.db import models
from adminapp.models import ForestOfficer


class EducationalVideo(models.Model):
    officer = models.ForeignKey(
        ForestOfficer,
        on_delete=models.CASCADE,
        related_name="videos"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    video = models.FileField(upload_to="educational_videos/")

    thumbnail = models.ImageField(upload_to="video_thumbnails/", blank=True, null=True)

    category = models.CharField(
        max_length=100,
        choices=[
            ("wildlife", "Wildlife Education"),
            ("environment", "Environmental Awareness"),
            ("forest_rules", "Forest Rules & Safety"),
            ("general", "General Education"),
        ],
        default="general"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "educational_videos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# models.py
from django.db import models
from adminapp.models import ForestOfficer

class WildlifeProtectionImage(models.Model):
    officer = models.ForeignKey(
        ForestOfficer,
        on_delete=models.CASCADE,
        related_name="protection_images"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="wildlife_protection/")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wildlife_protection_images"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
