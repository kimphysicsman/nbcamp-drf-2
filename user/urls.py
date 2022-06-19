from django.contrib import admin
from django.urls import path, include
from . import views

# user/
urlpatterns = [
    path('login/', views.UserApiView.as_view()),
    path('', views.UserView.as_view()),
]
