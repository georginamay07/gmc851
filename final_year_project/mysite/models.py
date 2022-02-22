from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    published_on = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')

       
    def publish(self):
        self.published_on=timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    
class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField()
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')
        
    def publish(self):
        self.save()

    def __str__(self):
        return self.title
    
       
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    comment = models.TextField()
    published_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.published_on=timezone.now()
        return str(self.comment)   
    
class Post(models.Model):
    artist = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')
    published_on = models.DateTimeField(blank=True, null=True)
    like = models.ManyToManyField(User, related_name='post_like')
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, related_name='comments')
    

    def __str__(self):
        self.published_on=timezone.now()
        return self.artist
    
    def publish(self):
        self.save()     
        
class Donation(models.Model):
    amount = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    first_name = models.TextField()
    last_name = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.user_id)
    
class Image(models.Model):
    fave_img = models.ImageField(upload_to='images/tiles/')
    
class BarberTile(models.Model):
    fave_image = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    amount = models.IntegerField()
    
    def __str__(self):
        return str(self.first_name)