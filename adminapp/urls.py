from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('', views.admin_officer_login, name='admin_officer_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # Category CRUD
    path('categories/', views.list_animal_category, name='list_animal_category'),
    path('categories/add/', views.add_animal_category, name='add_animal_category'),
    path('categories/edit/<int:category_id>/', views.edit_animal_category, name='edit_animal_category'),
    path('categories/delete/<int:category_id>/', views.delete_animal_category, name='delete_animal_category'),

    # Animal CRUD
    path('add-animal/', views.add_animal, name='add_animal'),
    path('view-animals/', views.view_animals, name='view_animals'),
    path('animal/<int:animal_id>/', views.view_animal_details, name='view_animal_details'),
    path('edit-animal/<int:animal_id>/', views.edit_animal, name='edit_animal'),
    path('delete-animal/<int:animal_id>/', views.delete_animal, name='delete_animal'),

   #Sanctuary Management
    path('add-wildlife-sanctuary/', views.add_wildlife_sanctuary, name='add_wildlife_sanctuary'),
    path('list-wildlife-sanctuary/', views.list_wildlife_sanctuary, name='list_wildlife_sanctuary'),
    path('view-wildlife-sanctuary/<int:sanctuary_id>/', views.view_sanctuary_details, name='view_sanctuary_details'),
    path('edit-sanctuary/<int:id>/', views.edit_wildlife_sanctuary, name='edit_wildlife_sanctuary'),
    path('delete-sanctuary/<int:id>/', views.delete_wildlife_sanctuary, name='delete_wildlife_sanctuary'),




    # Community Management
    path('add-community/', views.add_community, name='add_community'),
    path('list-community/', views.list_community, name='list_community'),
    path('edit-community/<int:pk>/', views.edit_community, name='edit_community'),
    path('delete-community/<int:pk>/', views.delete_community, name='delete_community'),


    #Topic management
    path('topics/', views.manage_topics, name='manage_topics'),


    #Journal list
    path('journals/', views.list_journals, name='list_journals'),
    path('journal/approve/<int:journal_id>/', views.approve_journal, name='approve_journal'),
    path('journal/reject/<int:journal_id>/', views.reject_journal, name='reject_journal'),


    #View users
    path('view-users/', views.view_users, name='view_users'),


    #Forest officers
    path('officers/add/', views.add_forest_officer, name="add_forest_officer"),
    path('officers/', views.list_forest_officers, name="list_forest_officers"),
    path('officers/edit/<int:officer_id>/', edit_forest_officer, name="edit_forest_officer"),
    path('officers/delete/<int:officer_id>/', delete_forest_officer, name="delete_forest_officer"),

    #Admin view recent sightings
    path("admin-view-recent-sightings/", admin_view_recent_sightings, name="admin_view_recent_sightings"),

    #Forest Dashboard
    path('forest_dashboard/',views.forest_dashboard,name='forest_dashboard'),
    path('officer/profile/', views.forest_officer_profile, name='forest_officer_profile'),
    path("profile/update/", views.update_officer_profile, name="update_officer_profile"),

    # Forest officer view sightings
    path("recent-sightings/", officer_recent_sightings, name="officer_recent_sightings"),

    #Poster Management
    path('officer/add-poster/', add_awareness_poster, name='add_awareness_poster'),
    path('officer/posters/', list_awareness_posters, name='list_awareness_posters'),
    path("officer/posters/edit/<int:poster_id>/", edit_awareness_poster, name="edit_awareness_poster"),
    path('officer/posters/delete/<int:poster_id>/', delete_awareness_poster, name='delete_awareness_poster'),



    path("videos/add/", views.add_educational_video, name="add_educational_video"),
    path("videos/list/", views.list_educational_videos, name="list_educational_videos"),
    path("videos/delete/<int:video_id>/", views.delete_educational_video, name="delete_educational_video"),
    path("videos/edit/<int:video_id>/", views.edit_educational_video, name="edit_educational_video"),


    path("add-protection-image/", add_protection_image, name="add_protection_image"),
    path("list-protection-images/", list_protection_images, name="list_protection_images"),
    path("edit-protection-image/<int:image_id>/", edit_protection_image, name="edit_protection_image"),
    path("delete-protection-image/<int:image_id>/", delete_protection_image, name="delete_protection_image"),
    




]
