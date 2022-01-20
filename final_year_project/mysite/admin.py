from django.contrib import admin

# Register your models here.

from .models import Posts, News, Events

admin.site.register(Posts)
admin.site.register(News)
admin.site.register(Events)