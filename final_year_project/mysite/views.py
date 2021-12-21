from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, 'mysite/homepage.html')

def news(request):
    return render(request, 'mysite/news.html')

def events(request):
    return render(request, 'mysite/events.html')

def donate(request):
    return render(request, 'mysite/donate.html')

def donate_tiles(request):
    return render(request, 'mysite/donate_tiles.html')

def login(request):
    return render(request, 'mysite/login.html')

def signup(request):
    return render(request, 'mysite/signup.html')