from django.contrib import admin
from .models import User, UserPorfile

# Register your models here.

admin.site.register(User)
admin.site.register(UserPorfile)