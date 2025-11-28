from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import  TblRegisterSerializer


class UserRegisterViewSet(viewsets.ModelViewSet):
    """API endpoint for user registration CRUD."""
    queryset = TblRegister.objects.all()
    serializer_class = TblRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_201_CREATED
        return response


@api_view(['POST'])
def user_login(request):
    """Handles user login API."""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = TblRegister.objects.get(username=username, password=password)
        serializer = TblRegisterSerializer(user)
        return Response({'message': 'Login successful', 'user': serializer.data}, status=status.HTTP_200_OK)
    except TblRegister.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework import generics
from rest_framework.permissions import AllowAny
from adminapp.models import WildAnimalCategory
from .serializers import UserViewCategorySerializer


class UserViewCategory(generics.ListAPIView):
    """
    API view for users to view all wild animal categories.
    """
    queryset = WildAnimalCategory.objects.all().order_by('name')
    serializer_class = UserViewCategorySerializer
    permission_classes = [AllowAny]



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import WildAnimal, WildAnimalCategory
from .serializers import (
    UserViewAnimalSerializer,
    UserViewAnimalByCategorySerializer,
)

# ✅ View all animals
@api_view(['GET'])
def user_view_animals(request):
    """
    API endpoint to view all wild animals.
    Supports optional search query (?q=) and category filter (?category_id=)
    """
    query = request.GET.get('q', '')
    category_id = request.GET.get('category_id', None)

    animals = WildAnimal.objects.all()

    if query:
        animals = animals.filter(name__icontains=query)

    if category_id:
        animals = animals.filter(category_id=category_id)

    serializer = UserViewAnimalSerializer(animals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ✅ View animals by category
@api_view(['GET'])
def user_view_animals_by_category(request, category_id):
    """
    API endpoint to view animals filtered by category ID.
    """
    try:
        category = WildAnimalCategory.objects.get(id=category_id)
    except WildAnimalCategory.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    animals = WildAnimal.objects.filter(category=category)
    serializer = UserViewAnimalByCategorySerializer(animals, many=True)
    return Response({
        "category": category.name,
        "animals": serializer.data
    }, status=status.HTTP_200_OK)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import TblWildLifeSanctuary
from .serializers import WildLifeSanctuarySerializer

class SanctuaryListView(APIView):
    def get(self, request):
        sanctuaries = TblWildLifeSanctuary.objects.prefetch_related('images').all().order_by('-created_at')
        serializer = WildLifeSanctuarySerializer(sanctuaries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SanctuaryDetailView(APIView):
    def get(self, request, pk):
        try:
            sanctuary = TblWildLifeSanctuary.objects.prefetch_related('images').get(pk=pk)
        except TblWildLifeSanctuary.DoesNotExist:
            return Response({'error': 'Sanctuary not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WildLifeSanctuarySerializer(sanctuary)
        return Response(serializer.data, status=status.HTTP_200_OK)



from adminapp.models import Community
from .serializers import CommunitySerializer
class userview_community(APIView):
    """API view to list all communities."""
    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import Community
from .serializers import CommunitySerializer

class CommunityBySanctuaryView(APIView):
    """List communities for a given sanctuary ID."""

    def get(self, request, sanctuary_id):
        communities = Community.objects.filter(sanctuary_id=sanctuary_id)

        if not communities.exists():
            return Response(
                {"message": "No communities found for this sanctuary"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import Community
from wildspotter_api.models import TblRegister  # Your user model

class JoinCommunityAPIView(APIView):
    """Allows a user to join a community."""

    def post(self, request, community_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            community = Community.objects.get(id=community_id)
            user = TblRegister.objects.get(id=user_id)
        except (Community.DoesNotExist, TblRegister.DoesNotExist):
            return Response({'error': 'Community or user not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user in community.joined_users.all():
            return Response({'message': 'User already joined this community.'}, status=status.HTTP_200_OK)

        community.joined_users.add(user)
        community.members = community.joined_users.count()
        community.save()

        return Response({'message': f'{user.name} joined {community.name} successfully!'}, status=status.HTTP_200_OK)


class LeaveCommunityAPIView(APIView):
    """Allows a user to leave a community."""

    def post(self, request, community_id):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            community = Community.objects.get(id=community_id)
            user = TblRegister.objects.get(id=user_id)
        except (Community.DoesNotExist, TblRegister.DoesNotExist):
            return Response({'error': 'Community or user not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user not in community.joined_users.all():
            return Response({'message': 'User is not a member of this community.'}, status=status.HTTP_400_BAD_REQUEST)

        community.joined_users.remove(user)
        community.members = community.joined_users.count()
        community.save()

        return Response({'message': f'{user.name} left {community.name} successfully.'}, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from adminapp.models import Topic
from .serializers import TopicSerializer

class UserViewTopics(APIView):
    """API view to list all topics."""

    def get(self, request):
        topics = Topic.objects.all().order_by('name')
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Journal
from adminapp.models import Topic
from .serializers import JournalSerializer

class CreateJournalAPIView(APIView):

    def post(self, request):
        user_id = request.data.get("user_id")
        topic_id = request.data.get("topic_id")
        name = request.data.get("name")
        description = request.data.get("description")
        status_value = request.data.get("status", "draft")

        if not user_id or not topic_id or not name:
            return Response({"error": "user_id, topic_id, and name are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = TblRegister.objects.get(id=user_id)
            topic = Topic.objects.get(id=topic_id)
        except:
            return Response({"error": "Invalid user or topic ID."},
                            status=status.HTTP_404_NOT_FOUND)

        journal = Journal.objects.create(
            user=user,
            topic=topic,
            name=name,
            description=description,
            status=status_value
        )

        serializer = JournalSerializer(journal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserJournalListAPIView(APIView):

    def get(self, request, user_id):
        journals = Journal.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = JournalSerializer(journals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Journal
from .serializers import JournalSerializer

@api_view(['GET'])
def get_published_journals(request):
    """API to fetch all published journals."""
    
    published_journals = Journal.objects.filter(status="Published").select_related("user", "topic")

    serializer = JournalSerializer(published_journals, many=True)

    return Response({
        "message": "Published journals retrieved successfully",
        "count": len(serializer.data),
        "data": serializer.data
    }, status=status.HTTP_200_OK)































































from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from google import genai
from google.genai import types # Import types for explicit schema definition
import os
from dotenv import load_dotenv
from PIL import Image
import io
import json # Used for parsing the model's JSON response

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# --- Initialize the Gemini Client ---
# The new SDK uses a Client object for all interactions.
# It automatically picks up the API key from environment variables (GOOGLE_API_KEY or GEMINI_API_KEY).
gemini_client = None
try:
    if not api_key:
        raise ValueError("❌ GOOGLE_API_KEY not found in .env file.")
    
    # Initialize the client. This is the modern, correct way.
    gemini_client = genai.Client(api_key=api_key)
    
except Exception as e:
    # Log the configuration error
    print(f"❌ Gemini Client Configuration Error: {e}")


# -------------------------------------------------------------
# Define the JSON Schema for the model's output
# This schema uses the types from the new SDK (`google.genai.types`)
# -------------------------------------------------------------
ANIMAL_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "name": types.Schema(type=types.Type.STRING),
        "scientific_name": types.Schema(type=types.Type.STRING),
        "food": types.Schema(type=types.Type.STRING, description="The animal's main diet."),
        "about": types.Schema(type=types.Type.STRING, description="A concise summary of the animal.")
    }
)


@csrf_exempt
def analyze_uploaded_image(request):
    """
    Analyzes an uploaded image file using the Gemini API and returns
    structured data about the predicted animal.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest(
            "Only POST requests are allowed for image analysis."
        )

    if not gemini_client:
        return JsonResponse(
            {"error": "Gemini API is not configured. Check the GOOGLE_API_KEY."},
            status=503
        )

    # 1. Get the uploaded file (Assuming form field name is 'image_file')
    uploaded_file = request.FILES.get('image_file')

    if not uploaded_file:
        return JsonResponse(
            {"error": "No image file provided in the 'image_file' field."},
            status=400
        )

    try:
        # 2. Convert Django InMemoryUploadedFile to PIL Image
        image_bytes = uploaded_file.read()
        pil_image = Image.open(io.BytesIO(image_bytes))

        # 3. Define the prompt
        prompt = (
            "Analyze the animal in this image. Respond with a single JSON object "
            "containing the fields: 'name', 'scientific_name', 'food', and 'about'. "
            "Do not include any text, notes, or markdown formatting outside of the JSON object itself."
        )

        # 4. Call the Gemini API for image analysis using the Client
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, pil_image],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ANIMAL_SCHEMA,
            )
        )

        # 5. Parse and return the structured response
        # response.text is guaranteed to be a valid JSON string due to the config
        analysis_result = json.loads(response.text)

        return JsonResponse(analysis_result, status=200)

    except Exception as e:
        print(f"An error occurred during API call or processing: {e}")
        return JsonResponse(
            {"error": f"Failed to analyze image: {type(e).__name__}: {str(e)}"},
            status=500
        )
    



class RecentSightingView(APIView):

    def post(self, request):
        serializer = RecentSightingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Recent sighting added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RecentSighting
from .serializers import RecentSightingSerializer

class LatestRecentSightingView(APIView):

    def get(self, request):
        # Get latest 3
        latest_sightings = RecentSighting.objects.select_related(
            "user", "sanctuary"
        ).order_by("-created_at")[:3]

        serializer = RecentSightingSerializer(latest_sightings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RecentSighting
from .serializers import RecentSightingSerializer

class RecentSightingBySanctuaryView(APIView):

    def get(self, request, sanctuary_id):
        sightings = RecentSighting.objects.filter(
            sanctuary_id=sanctuary_id
        ).select_related("user", "sanctuary").order_by("-created_at")

        serializer = RecentSightingSerializer(sightings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RecentSighting
from .serializers import RecentSightingSerializer

class RecentSightingByUserView(APIView):

    def get(self, request, user_id):
        sightings = RecentSighting.objects.filter(
            user_id=user_id
        ).select_related("user", "sanctuary").order_by("-created_at")

        serializer = RecentSightingSerializer(sightings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)










from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from adminapp.models import WildlifeProtectionImage, AwarenessPoster, EducationalVideo
from .serializers import (
    WildlifeProtectionImageSerializer,
    AwarenessPosterSerializer,
    EducationalVideoSerializer
)


#  View Wildlife Protection Images
class WildlifeProtectionImagesAPI(APIView):
    def get(self, request):
        images = WildlifeProtectionImage.objects.select_related("officer")
        serializer = WildlifeProtectionImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#  View Awareness Posters
class AwarenessPostersAPI(APIView):
    def get(self, request):
        posters = AwarenessPoster.objects.select_related("officer")
        serializer = AwarenessPosterSerializer(posters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#  View Educational Videos
class EducationalVideosAPI(APIView):
    def get(self, request):
        videos = EducationalVideo.objects.select_related("officer")
        serializer = EducationalVideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from adminapp.models import WildlifeProtectionImage, AwarenessPoster, EducationalVideo
from .serializers import (
    WildlifeProtectionImageSerializer,
    AwarenessPosterSerializer,
    EducationalVideoSerializer
)


# 1️⃣ Wildlife Protection Images by Sanctuary
class WildlifeProtectionBySanctuaryAPI(APIView):
    def get(self, request, sanctuary_id):
        images = WildlifeProtectionImage.objects.filter(
            officer__sanctuary_id=sanctuary_id
        )

        serializer = WildlifeProtectionImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 2️⃣ Awareness Posters by Sanctuary
class AwarenessPostersBySanctuaryAPI(APIView):
    def get(self, request, sanctuary_id):
        posters = AwarenessPoster.objects.filter(
            officer__sanctuary_id=sanctuary_id
        )

        serializer = AwarenessPosterSerializer(posters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 3️⃣ Educational Videos by Sanctuary
class EducationalVideosBySanctuaryAPI(APIView):
    def get(self, request, sanctuary_id):
        videos = EducationalVideo.objects.filter(
            officer__sanctuary_id=sanctuary_id
        )

        serializer = EducationalVideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from .models import SightingRating
from .serializers import SightingRatingSerializer

class AddSightingRatingAPI(APIView):
    
    def post(self, request):
        user = request.data.get("user")
        sighting = request.data.get("sighting")
        rating = request.data.get("rating")

        if not all([user, sighting, rating]):
            return Response({"error": "user, sighting and rating are required"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # If rating exists → update
        try:
            existing = SightingRating.objects.get(user=user, sighting=sighting)
            existing.rating = rating
            existing.save()
            serializer = SightingRatingSerializer(existing)
            return Response({
                "message": "Rating updated successfully",
                "data": serializer.data
            })
        except SightingRating.DoesNotExist:
            pass

        # Create new rating
        serializer = SightingRatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Rating added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SightingRating
from .serializers import SightingRatingSerializer

class ViewSightingRatingsAPI(APIView):

    def get(self, request, sighting_id):
        ratings = SightingRating.objects.filter(sighting_id=sighting_id)

        if not ratings.exists():
            return Response(
                {"message": "No ratings found for this sighting."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SightingRatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewUserRatingsAPI(APIView):

    def get(self, request, user_id):
        ratings = SightingRating.objects.filter(user_id=user_id)

        if not ratings.exists():
            return Response(
                {"message": "This user has not rated any sightings."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SightingRatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAllRatingsAPI(APIView):

    def get(self, request):
        ratings = SightingRating.objects.all()
        serializer = SightingRatingSerializer(ratings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
