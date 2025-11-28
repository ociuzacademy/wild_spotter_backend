from rest_framework import serializers
from .models import RecentSighting, TblRegister
from adminapp.models import *

class TblRegisterSerializer(serializers.ModelSerializer):
    """Serializer for the TblRegister model."""
    class Meta:
        model = TblRegister
        fields = '__all__'




class UserViewCategorySerializer(serializers.ModelSerializer):
    """Serializer for viewing wild animal categories."""
    class Meta:
        model = WildAnimalCategory
        fields = '__all__'


class UserViewAnimalSerializer(serializers.ModelSerializer):
    """Serializer for viewing wild animals."""
    category = UserViewCategorySerializer(read_only=True)

    class Meta:
        model = WildAnimal
        fields = '__all__'

class UserViewAnimalByCategorySerializer(serializers.ModelSerializer):
    """Serializer for viewing wild animals by category."""
    class Meta:
        model = WildAnimal
        fields = '__all__'



from rest_framework import serializers
from adminapp.models import TblWildLifeSanctuary, TblSanctuaryImage

from rest_framework import serializers
from adminapp.models import TblWildLifeSanctuary, TblSanctuaryImage


class SanctuaryImageSerializer(serializers.ModelSerializer):
    """Serializer for individual sanctuary images."""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TblSanctuaryImage
        fields = ['id', 'image_url', 'caption', 'uploaded_at']

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            # Return relative path from /media/
            return obj.image.url
        return None


class WildLifeSanctuarySerializer(serializers.ModelSerializer):
    """Serializer for sanctuary with nested images."""
    images = SanctuaryImageSerializer(many=True, read_only=True)

    class Meta:
        model = TblWildLifeSanctuary
        fields = [
            'id', 'name', 'species_count', 'hectare', 'viewpoints',
            'visitors_per_month', 'about', 'created_at', 'images'
        ]




from adminapp.models import Community
class CommunitySerializer(serializers.ModelSerializer):
    sanctuary_name = serializers.CharField(source='sanctuary.name', read_only=True)
    picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'sanctuary', 'sanctuary_name',
            'picture', 'picture_url', 'members', 'created_at'
        ]

    def get_picture_url(self, obj):
        if obj.picture:
            return obj.picture.url
        return None



from rest_framework import serializers
from adminapp.models import Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']



from rest_framework import serializers
from adminapp.models import Topic
# from userapp.models import tbl_register
from .models import Journal

class JournalSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = Journal
        fields = [
            'id',
            'user',
            'user_name',
            'topic',
            'topic_name',
            'name',
            'description',
            'status',
            'created_at',
        ]


from .models import RecentSighting
class RecentSightingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = RecentSighting
        fields = "__all__"

    def get_average_rating(self, obj):
        from django.db.models import Avg
        return obj.ratings.aggregate(
            Avg("rating")
        )["rating__avg"]




from rest_framework import serializers
from adminapp.models import WildlifeProtectionImage, AwarenessPoster, EducationalVideo


#  Wildlife Protection Images Serializer
class WildlifeProtectionImageSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source="officer.name", read_only=True)

    class Meta:
        model = WildlifeProtectionImage
        fields = [
            "id",
            "officer",
            "officer_name",
            "title",
            "description",
            "image",
            "created_at"
        ]


#  Awareness Posters Serializer
class AwarenessPosterSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source="officer.name", read_only=True)

    class Meta:
        model = AwarenessPoster
        fields = [
            "id",
            "officer",
            "officer_name",
            "title",
            "description",
            "image",
            "category",
            "created_at"
        ]


# 3️ Educational Videos Serializer
class EducationalVideoSerializer(serializers.ModelSerializer):
    officer_name = serializers.CharField(source="officer.name", read_only=True)

    class Meta:
        model = EducationalVideo
        fields = [
            "id",
            "officer",
            "officer_name",
            "title",
            "description",
            "video",
            "thumbnail",
            "category",
            "created_at"
        ]

# serializers.py
from rest_framework import serializers
from .models import RecentSighting
from .models import SightingRating

class SightingRatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    sighting_species = serializers.CharField(source="sighting.species", read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = SightingRating
        fields = [
            "id",
            "user",
            "user_name",
            "sighting",
            "sighting_species",
            "rating",
            "average_rating",
            "created_at",
        ]

    def get_average_rating(self, obj):
        return obj.sighting.ratings.aggregate(models.Avg("rating"))["rating__avg"]
