from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
import sorl.thumbnail
# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

#Comment model
#Has three fields
#--user id which is a foreign key 
#--comment which is the comment
#--published on which is when it was published

class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    comment = models.TextField()
    published_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        self.published_on=timezone.now()
        return str(self.comment)    
    
#Article model
#Has five fields
#--title which is the title of the article
#--published on which is when the article was published
#--content which is the main text of the article
#--cover image which is the picture displayed alongside the article
#--comments which is a many to many field - an article can have many comments

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    published_on = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')
    comments = models.ManyToManyField(Comment, related_name='news_comments', blank=True)


       
    def publish(self):
        self.published_on=timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
#Event Model
#Has four fields
#--title which is the title of the event
#--date which is the date of the event
#--content which is the main text of the event
#--cover image which is the picture displayed alongside the event

class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField()
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')
        
    def publish(self):
        self.save()

    def __str__(self):
        return self.title
    
#Post Model
#Has eight fields
#--artist which is the artist's name and dates
#--content which is the posts description
#--cover image which is the artwork
#--published on which is when the post was published
#--like which is a many to many field - a post can have many likes by many users
#--number of likes which counts the number of likes for a post
#--tags which describe the post
#--comments which is a many to many field - a post can have many comments
 
class Post(models.Model):
    artist = models.CharField(max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/')
    published_on = models.DateTimeField(blank=True, null=True)
    like = models.ManyToManyField(User, related_name='post_like', blank=True)
    number_of_likes = models.IntegerField(default=0)
    tags = TaggableManager()
    comments = models.ManyToManyField(Comment, related_name='comments', blank=True)
    

    def __str__(self):
        self.published_on=timezone.now()
        return self.artist
    
    def publish(self):
        self.save()     
        
#Donation Model
#Has five fields
#--amount which is the donation amount - 1,5 or 10
#--user id which is a foreign key 
#--first name which is the users first name
#--last name which is the users last name
#--date which is the date they made the donation

class Donation(models.Model):
    amount = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    first_name = models.TextField()
    last_name = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.user_id)
    
#Image Model
#Has one field
#--fave image which is the users current fave image to display on their tile

class Image(models.Model):
    fave_img = models.ImageField(upload_to='images/tiles/')
    
#Tile Model
#Has four fields
#--fave image which is the tile's image
#--first name which is the users first name
#--last name which is the users last name
#--amount which is the donation amount - 1,5 or 10

class BarberTile(models.Model):
    fave_image = models.ImageField()
    first_name = models.TextField()
    last_name = models.TextField()
    amount = models.IntegerField()
    
    def __str__(self):
        return str(self.first_name)
    
#Liked Tags Model
#Has two fields
#--user id which is a foreign key
#--tags which is the users liked tags

class LikedTag(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    tags = TaggableManager()

    def __str__(self):
        return str(self.user_id)
