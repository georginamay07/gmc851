from django.contrib import admin

# Register your models here.

from .models import Post, Article, Event, Donation, Comment, BarberTile

admin.site.register(Post)
admin.site.register(Article)
admin.site.register(Event)
admin.site.register(Donation)
admin.site.register(Comment)
admin.site.register(BarberTile)
