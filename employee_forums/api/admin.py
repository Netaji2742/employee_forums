from django.contrib import admin

# Register your models here.


#from django.contrib import admin
from .models import UserProfile, Post, Like, Connection

# Register models
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Connection)
