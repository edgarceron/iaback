"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views

urlpatterns = [
    path('search_images', views.search_images, name='search_images'),
]
