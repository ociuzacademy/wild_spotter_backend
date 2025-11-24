from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import UserRegisterViewSet, user_login
from .views import *
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="WildSpotter API",
        default_version='v1',
        description="API documentation for WildSpotter App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'register', UserRegisterViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', user_login, name='user_login'),
    path('categories/', UserViewCategory.as_view(), name='user_view_category'),
    path('user/view-animals/', views.user_view_animals, name='user_view_animals'),
    path('user/view-animals/category/<int:category_id>/', views.user_view_animals_by_category, name='user_view_animals_by_category'),
    path('sanctuaries/', SanctuaryListView.as_view(), name='sanctuary-list'),
    path('sanctuaries/<int:pk>/', SanctuaryDetailView.as_view(), name='sanctuary-detail'),
    path('communities/', userview_community.as_view(), name='user_view_community'),
    path('community/<int:community_id>/join/', JoinCommunityAPIView.as_view(), name='join_community'),
    path('community/<int:community_id>/leave/', LeaveCommunityAPIView.as_view(), name='leave_community'),
    path('topics/', UserViewTopics.as_view(), name='user_topics'),
    path('journal/create/', CreateJournalAPIView.as_view(), name='create_journal'),
    path('journal/user/<int:user_id>/', UserJournalListAPIView.as_view(), name='user_journals'),
    path("journals/published/", get_published_journals, name="get_published_journals"),
    path('predict_animal/',analyze_uploaded_image,name='analyze_uploaded_image'),
    path('communities/<int:sanctuary_id>/', CommunityBySanctuaryView.as_view(), name='community_by_sanctuary'),
    path("recent-sightings/", RecentSightingView.as_view(), name="recent_sightings"),
    path("recent-sightings/latest/", LatestRecentSightingView.as_view(), name="latest_recent_sightings"),
    path("recent-sightings/sanctuary/<int:sanctuary_id>/",RecentSightingBySanctuaryView.as_view(),name="recent_sightings_by_sanctuary"),
    path("recent-sightings/user/<int:user_id>/",RecentSightingByUserView.as_view(),name="recent_sightings_by_user"),
    path("wildlife-protection-images/", WildlifeProtectionImagesAPI.as_view(), name="api_wildlife_protection"),
    path("awareness-posters/", AwarenessPostersAPI.as_view(), name="api_awareness_posters"),
    path("educational-videos/", EducationalVideosAPI.as_view(), name="api_educational_videos"),
    path("wildlife-protection/<int:sanctuary_id>/", WildlifeProtectionBySanctuaryAPI.as_view(), name="api_wildlife_protection_by_sanctuary"),
    path("awareness-posters/<int:sanctuary_id>/", AwarenessPostersBySanctuaryAPI.as_view(), name="api_awareness_posters_by_sanctuary"),
    path("educational-videos/<int:sanctuary_id>/", EducationalVideosBySanctuaryAPI.as_view(), name="api_educational_videos_by_sanctuary"),
    path("rate-sighting/", AddSightingRatingAPI.as_view(), name="rate_sighting"),
     path("sighting/<int:sighting_id>/ratings/", ViewSightingRatingsAPI.as_view(), name="view_sighting_ratings"),
    path("user/<int:user_id>/ratings/", ViewUserRatingsAPI.as_view(), name="view_user_ratings"),
    path("ratings/", ViewAllRatingsAPI.as_view(), name="view_all_ratings"),
    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
