from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class News(models.Model):
    title = models.CharField(max_length=200, unique=True)
    published_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ['-published_on']

    def __str__(self):
        return self.title
    
    
class Events(models.Model):
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField()
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
    
    
class Posts(models.Model):
    artist = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title