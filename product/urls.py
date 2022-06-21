from django.contrib import admin
from django.urls import path, include
from . import views

# product/
urlpatterns = [
    path('', views.ProductView.as_view()),
]