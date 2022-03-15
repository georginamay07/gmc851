from datetime import date
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import ImageForm, SignUpForm
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Count
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

#Import all models

from .models import Article
from .models import Event
from .models import Post
from .models import User
from .models import Donation
from .models import Comment
from .models import LikedTag
from .models import BarberTile

#---Views---#
#Certain views are forbidden to access by users if they are not logged in

#Homepage 
#--Displays all posts ordered by published date

@login_required(login_url='forbidden')
def home(request):
    #POST REQUEST
    if request.method == 'POST':
        #gets the current post
        post_id = request.POST.get('pk')
        #if users clicks sumbit comment
        if 'comment_submit' in request.POST:
            submitPostComment(request, post_id)
        #if user clicks delete comment
        if 'delete_comment' in request.POST:
            deleteComment(request)
        #if user clicks like
        if 'like' in request.POST:
            #this function likes the post
            likePost(request,post_id)
            #this function adds the posts tags to the users liked tags
            addLikeTags(request,post_id)
        #if user clicks unlike
        if 'unlike' in request.POST:
            #this function unlikes the post
            unlikePost(request,post_id)
            #this function removes the posts tags from the users liked tags
            removeLikeTags(request,post_id)
    #GET REQUEST
    #gets all posts and orders them by published date starting with the most recent
    posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    url = "newist"
    #this renders the html page
    return render(request, 'mysite/homepage.html', {'posts':posts, 'url':url})

#Homepage 
#--Displays all posts ordered by like count

@login_required(login_url='forbidden')
def home_like(request):
    #POST REQUEST
    if request.method == 'POST':
        #gets the current post
        post_id = request.POST.get('pk')
        #if users clicks sumbit comment
        if 'comment_submit' in request.POST:
            submitPostComment(request, post_id)
        #if user clicks delete comment
        if 'delete_comment' in request.POST:
            deleteComment(request)
        #if user clicks like
        if 'like' in request.POST:
            #this function likes the post
            likePost(request,post_id)
            #this function adds the posts tags to the users liked tags
            addLikeTags(request,post_id)
        #if user clicks unlike
        if 'unlike' in request.POST:
            #this function unlikes the post
            unlikePost(request,post_id)
            #this function removes the posts tags from the users liked tags
            removeLikeTags(request,post_id)
    #GET REQUEST
    #gets all posts and orders them by number of likes starting with the most
    posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('-number_of_likes')
    url = "like"
    #this renders the html page
    return render(request, 'mysite/homepage.html', {'posts':posts,'url':url})

#Homepage 
#--Displays recommended posts

@login_required(login_url='forbidden')
def home_recommended(request):
    #POST REQUEST
    if request.method == 'POST':
        #gets the current post
        post_id = request.POST.get('pk')
        #if users clicks sumbit comment
        if 'comment_submit' in request.POST:
            submitPostComment(request, post_id)
        #if user clicks delete comment
        if 'delete_comment' in request.POST:
            deleteComment(request)
        #if user clicks like
        if 'like' in request.POST:
            #this function likes the post
            likePost(request,post_id)
            #this function adds the posts tags to the users liked tags
            addLikeTags(request,post_id)
        #if user clicks unlike
        if 'unlike' in request.POST:
            #this function unlikes the post
            unlikePost(request,post_id)
            #this function removes the posts tags from the users liked tags
            removeLikeTags(request,post_id)
    #GET REQUEST
    posts=None
    #if the user already has liked tags, we can recommend posts
    if(LikedTag.objects.filter(user_id=request.user).exists()):
        #gets all of the users liked tags
        user_tags = LikedTag.objects.get(user_id=request.user).tags.all()
        tag_list=[]
        i = 0
        #adds users liked tags to a list
        for item in user_tags:
            tag = str(user_tags[i])
            tag_list.append(tag)
            i+=1
            #checks if user tags is empty, if so, then we cannot recommend anything
            if not user_tags:
                posts=None
            #gets all posts
            #does not include posts that have been liked by the user
            #includes posts that include a tag that the user likes
            #posts with no similar tags are displayed last
            else:
                posts = Post.objects.filter(~Q(like=request.user)).annotate(similar_tags=Count('tags', filter=Q(tags__in=user_tags))).order_by('-similar_tags')
    #if the user has no liked tags, then we cannot recommend anything
    else:
        posts=None
    url = "recommended"
    #this renders the html page
    return render(request, 'mysite/homepage.html', {'posts':posts, 'url':url})
    
#News
#--This displays all the news articles 

@login_required(login_url='forbidden')
def news(request):
    #POST REQUEST
    if request.method == 'POST':
        #gets the current news article
        article_id = request.POST.get('pk')
        #if the user clicks submit comment
        if 'comment_submit' in request.POST:      
            submitArticleComment(request, article_id)  
        #if the user clicks delete comment    
        if 'delete_comment' in request.POST:
            deleteComment(request)
    #GET REQUEST
    #gets all news articles and orders them by published date, with the most recent first
    articles = Article.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    #this renders the html page
    return render(request, 'mysite/news.html', {'articles':articles})

#Events
#--This displays all the events

@login_required(login_url='forbidden')
def events(request):
    #GET REQUEST
    #gets all events and orders them by event date, with the first upcoming event showing first
    events = Event.objects.order_by('date')
    #this renders the html page
    return render(request, 'mysite/events.html', {'events': events})

#Donate
#--This displays the donation page and donation options

@login_required(login_url='forbidden')
def donate(request):
    #GET REQUEST
    form = ImageForm(request.POST, request.FILES)
    #POST REQUEST
    if request.method == "POST": 
        #if user clicks submit image
        if 'image_donation' in request.POST:
            if form.is_valid():
                #save the image to images/tiles
                form.save() 
                #get the name of the uploaded image
                fave_img = request.FILES['fave_img'].name
                #renders the html page and displays the current uploaded image
                return render(request, 'mysite/donate.html', {'fave_img':fave_img, 'form':form})
        #if user clicks Paypal
        else:
            #get data from the requests body which includes amount and fave image
            data=request.body   
            #convert data to a json   
            json_data = json.loads(str(data, encoding='utf-8'))
            
            #if the user has donated £1
            
            if json_data['amount'] == '1':
                #create a donation object in the database with the donation amount and users name
                #if users chooses to not upload their favourite image, their donation is still recorded, but no tile is created
                Donation.objects.create(amount=1, user_id=request.user, first_name=request.user.first_name, last_name=request.user.last_name)
                #if the user has uploaded an image
                if json_data['fave_image'] != '':
                    url = "images/tiles/" + json_data['fave_image']
                    #create a tile with the favourite image, users name and donation amount
                    BarberTile.objects.create(fave_image=url,first_name=request.user.first_name, last_name=request.user.last_name, amount=1)
            #if the user has donated £5

            if json_data['amount'] == '5':
                Donation.objects.create(amount=5, user_id=request.user, first_name=request.user.first_name, last_name=request.user.last_name)
                if json_data['fave_image'] != '':
                    url = "images/tiles/" + json_data['fave_image']
                    BarberTile.objects.create(fave_image=url,first_name=request.user.first_name, last_name=request.user.last_name, amount=5)
            #if the user has donated £10

            if json_data['amount'] == '10':
                Donation.objects.create(amount=10, user_id=request.user, first_name=request.user.first_name, last_name=request.user.last_name) 
                if json_data['fave_image'] != '':
                    url = "images/tiles/" + json_data['fave_image']
                    BarberTile.objects.create(fave_image=url,first_name=request.user.first_name, last_name=request.user.last_name, amount=10)
    #GET REQUEST
    else:
        form = ImageForm()
    #renders the html page
    return render(request, 'mysite/donate.html', {'form':form})


#Barber Tiles
#--Displays the virtual tile wall

@login_required(login_url='forbidden')
def donate_tiles(request):
    #gets all tiles
    tiles = BarberTile.objects.prefetch_related().all()
    #renders the html page
    return render(request, 'mysite/donate_tiles.html', {'tiles': tiles})

#Donation Success
#--Displays if the users donation has gone through paypal successfully

@login_required(login_url='forbidden')
def donate_success(request):
    return render(request, 'mysite/donate_success.html')

#Donation History
#--Displays the users history of donations

@login_required(login_url='forbidden')
def donate_history(request):
    #gets all donations
    donations = Donation.objects.prefetch_related().all()
    user_donations = None
    #gets only the current users donations
    for i in donations:
        user_donations = Donation.objects.filter(user_id = request.user)
    #renders the html page
    return render(request, 'mysite/donation_history.html', {'user_donations': user_donations})

#Liked Posts
#--Displays the users current liked posts

@login_required(login_url='forbidden')
def liked_posts(request):
    #POST REQUEST
    if request.method == 'POST':
        #gets the current post
        post_id = request.POST.get('pk')
        #if user clicks unlike
        if 'unlike' in request.POST:
            #function to unlike the post
            unlikePost(request,post_id)
            #function that removes the posts tags from the users liked tags
            removeLikeTags(request,post_id)
    #GET REQUEST
    #gets all posts
    posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    #gets only posts that have been liked by the user
    for i in posts:
        liked_posts = Post.objects.filter(like = request.user)
    #renders the html page
    return render(request, 'mysite/liked_posts.html', {'liked_posts':liked_posts})

#Login
#--This deals with user login

def my_login(request):
    #messages are used to show if the user has failed to login for any reason
    messages=""
    #POST REQUEST
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            #gets the data the user has entered
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            #built in function that authenticates the user
            #password is encrypted using SHA256
            user = authenticate(username=username, password=password)
            if user is not None:
                #this logs the user in
                login(request, user)
                #redirects them to the homepage
                return redirect('home')
        else:                  
            messages = "Invalid email or password"
    #GET REQUEST
    #Display empty form
    form = AuthenticationForm()
    #renders the html page
    return render(request=request, template_name='mysite/login.html', context={"login_form":form, 'messages':messages})

#Logout
#--This deals with user logout

def my_logout(request):
    #logs the user out
    logout(request)
    #redirects the user back to the login page
    return redirect('login')

#Sign Up
#--This deals with creating a user account

def signup(request): 
    #messages are used to show if the user has failed to login for any reason
    messages=""
    #POST REQUEST
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            #saves the users data to the form
            form.save()
            #if valid it redirects the user to successful sign up
            return redirect('successful_signup')
        #failed message
        messages="Unsuccessful registration"
    #GET REQUEST
    #displays an empty form
    else:
        form = SignUpForm()
    #renders the html page
    return render(request=request, template_name='mysite/signup.html', context={"signup_form":form,'messages':messages})

#Successful Sign Up
#--Displayed if user has successfully signed up

def successful_signup(request):
    return render(request, 'mysite/successful_signup.html')

#Password Reset
#--Deals with users forgetting their password

def password_reset(request, *args, **kwargs):
    #POST REQUEST
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            #gets the users email from the form
            email = form.cleaned_data['email']
            #gets all users with that email fromt he database
            assoc_users = User.objects.filter(Q(email=email))
            #if a users exists with this email
            if assoc_users.exists():
                #loops through each user with this email address and sends them an email
                for user in assoc_users:
                    subject = "You requested a password reset - Barber Institute"
                    email_template_name = 'mysite/email_template.txt'
                    #variables used in the email template
                    #uid encodes the users id
                    #generates a unique token that can only be used once
                    c = {"email": user.email, "domain": '127.0.0.1:8000', "site_name": 'The Barber Institute', 
                         "uid": urlsafe_base64_encode(force_bytes(user.pk)), 
                         "user":user, "token": default_token_generator.make_token(user), 
                         "protocol":"http",}
                    #renders the email 
                    email = render_to_string(email_template_name, c)
                    #trys to send the email
                    try:
                        send_mail(subject, email, 'barberinstiutetest@gmail.com', [user.email],fail_silently=False)
                    #if it faile to send
                    except BadHeaderError:
                        return HttpResponse('Invalid Header')
                    #redirect user to tell them a password reset email has been sent
                    return redirect('password_reset_sent')
    #GET REQUEST
    #Displays an empty form
    form = PasswordResetForm()
    #renders the html page
    return render(request=request, template_name='mysite/forgotten_password.html', context={"password_reset_form":form})

#Forbidden Page
#Deals with pages that cannot be displayed if user is not logged in

def forbidden(request):
    return render(request, 'mysite/forbidden_page.html')



#---Functions---#

#Deals with users submitting a comment
def submitPostComment(request, post_id):
    #gets the comment from the textarea
    comment = request.POST['comment']
    #creates a comment object in the database
    comment_instance = Comment.objects.create(user_id = request.user, comment= comment)    
    #get the current post
    this_post = Post.objects.get(id=post_id)
    #add this comment to the current post
    this_post.comments.add(Comment.objects.get(id=comment_instance.id))  
    
#Deals with users deleting their own comments
def deleteComment(request):
    #get the id of the comment to be deleted
    deleted_comment = request.POST.get('comment_pk')
    #get the comment object with this id
    delete_comment_instance = Comment.objects.get(user_id = request.user, id = deleted_comment)    
    #delete the comment, which will also remove it from the post
    delete_comment_instance.delete()

#Deals with users submitting comments on articles
def submitArticleComment(request, article_id):
    comment = request.POST['comment']
    comment_instance = Comment.objects.create(user_id = request.user, comment= comment)    
    this_article= Article.objects.get(id=article_id)    
    this_article.comments.add(Comment.objects.get(id=comment_instance.id))  

#Deals with users liking posts
def likePost(request, post_id):
    #gets the current post
    this_post = Post.objects.get(id=post_id)
    #increasing the number of likes by 1
    this_post.number_of_likes += 1
    #saves the post
    this_post.save()
    #adds the like to the post
    this_post.like.add(request.user)
    
#Deals with users unliking posts
def unlikePost(request,post_id):
    #gets the current post
    this_post = Post.objects.get(id=post_id) 
    #decreases the number of likes by 1   
    this_post.number_of_likes -= 1
    #saves the post
    this_post.save()
    #removes the users like from the post
    this_post.like.remove(request.user)  
    
#Deals with adding tags to users liked tags
def addLikeTags(request,post_id):
    #gets the current ;ost
    this_post = Post.objects.get(id=post_id)
    #gets the posts tags
    post_tags = this_post.tags.all()
    i = 0
    #if user has got a liked tag object already
    if(LikedTag.objects.filter(user_id =request.user).exists()):
        #get the existing object
        liked_tags_instance = LikedTag.objects.get(user_id=request.user)
        #for each post tag, add to users liked tags
        for item in post_tags:
            tag = str(post_tags[i])
            liked_tags_instance.tags.add(tag)
            i+=1
    #if user does not have a liked tag object
    else:
        #create a liked tag object for that user
        liked_tags_instance = LikedTag.objects.create(user_id=request.user)
        #for each post tag, add to users liked tags
        for item in post_tags:
            tag = str(post_tags[i])
            liked_tags_instance.tags.add(tag)
            i+=1
            
#Deals with removing tags from users liked tags
def removeLikeTags(request, post_id):
    #gest the current post
    this_post = Post.objects.get(id=post_id)  
    #gets the posts tags   
    post_tags = this_post.tags.all()
    i = 0
    #gets the users liked tags object
    liked_tags_instance = LikedTag.objects.get(user_id=request.user)
    #for each post tag, remove from users liked tags
    for item in post_tags:
        tag = str(post_tags[i])
        liked_tags_instance.tags.remove(tag)
        i+=1       
        
