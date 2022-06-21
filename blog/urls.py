from django.contrib import admin
from django.urls import path, include
from . import views

# blog/
urlpatterns = [
    path('article/', views.UserArticle.as_view()),
]
