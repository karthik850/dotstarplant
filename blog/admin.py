from django.contrib import admin
from .models import posts,comments,savedposts

# Register your models here.

admin.site.register(posts)
admin.site.register(comments)
admin.site.register(savedposts)