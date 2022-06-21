from datetime import timedelta
from django.db import models
from user.models import User as UserModel

class Product(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    show_start_at = models.DateTimeField(default="2022-06-20 00:00:00")
    show_end_at = models.DateTimeField(default="2022-06-25 00:00:00")
    thumbnail = models.ImageField(upload_to='product/img', height_field=None, width_field=None, max_length=100)
    
    def __str__(self):
        return f'Product : {self.title} - {self.author}'
