from tkinter import CASCADE
from django.db import models
from user.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    explain = models.TextField()

    def __str__(self):
        return self.category_name


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return f'{self.title} - {self.author}'


