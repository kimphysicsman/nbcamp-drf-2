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
    thumbnail = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    
    def __str__(self):
        return f'Product : {self.title} - {self.author}'

    def image_tag(self):
        from django.utils.html import escape
        return u'<img src="%s" />' % escape('https://www.notion.so/image/https%3A%2F%2Fpost-phinf.pstatic.net%2FMjAxOTA5MjZfNzEg%2FMDAxNTY5NDY2MzY5MzM0.FxfbYJ-W2f0YttSaWjQRg-tcApxpLWx1R8lccTCT4zgg.5Q4VvR0HY_KYUUuVMBf14sAk-eOS3RBqOJKfm29LNSEg.JPEG%2F%25EB%25AC%25BB%25EA%25B3%25A0_%25EB%2596%25A0%25EB%25B8%2594%25EB%259F%25AC_%25EA%25B0%2580.jpg%3Ftype%3Dw1200?table=block&id=c72ec1ae-8d9a-4f9f-ba34-7276e7d1839c&spaceId=18a55a3f-2515-4f20-9f7f-04187576573f&width=250&userId=f65f0c54-5dc8-4f1b-acf4-e4d6d5c93a82&cache=v2')
    
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True