from django.contrib import admin

# Register your models here.

from .models import Post, Article, Event

admin.site.register(Post)
admin.site.register(Article)
admin.site.register(Event)