from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Article
from .models import Event
from .models import Post
from django.utils import timezone

def home(request):
    posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    return render(request, 'mysite/homepage.html', {'posts': posts})

def news(request):
    articles = Article.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    return render(request, 'mysite/news.html', {'articles':articles})

def events(request):
    events = Event.objects.order_by('date')
    return render(request, 'mysite/events.html', {'events': events})

def donate(request):
    return render(request, 'mysite/donate.html')

def donate_tiles(request):
    return render(request, 'mysite/donate_tiles.html')

def login(request):
    return render(request, 'mysite/login.html')

def signup(request):
    return render(request, 'mysite/signup.html')