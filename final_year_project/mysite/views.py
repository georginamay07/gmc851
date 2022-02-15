from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import requests
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponseRedirect


from .models import Article
from .models import Event
from .models import Post
from .models import User
from .models import Donation
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse

@login_required(login_url='forbidden')
def home(request):
    posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    return render(request, 'mysite/homepage.html', {'posts': posts})

@login_required(login_url='forbidden')
def news(request):
    articles = Article.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    return render(request, 'mysite/news.html', {'articles':articles})

@login_required(login_url='forbidden')
def events(request):
    events = Event.objects.order_by('date')
    return render(request, 'mysite/events.html', {'events': events})

@login_required(login_url='forbidden')
def donate(request):
    #Donation.objects.create(amount=request.GET.get('value'), fave_image=request.GET.get('img'), first_name=User.first_name, last_name=User.last_name)
    return render(request, 'mysite/donate.html')

@login_required(login_url='forbidden')
def donate_tiles(request):
    return render(request, 'mysite/donate_tiles.html')

@login_required(login_url='forbidden')
def donate_history(request):
    donations = Donation.objects.prefetch_related().all()
    for i in donations:
        user_donations = Donation.objects.filter(user_id = request.user)
    return render(request, 'mysite/donation_history.html', {'user_donations': user_donations})

@login_required(login_url='forbidden')
def liked_posts(request):
    posts = Post.objects.filter(published_on__lte=timezone.now()).order_by('published_on')
    return render(request, 'mysite/liked_posts.html', {'posts':posts})

def my_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:                  
            messages.error(request, "Invalid email or password")
    else:
        messages.error(request, "Invalid email or password")
    form = AuthenticationForm()
    return render(request=request, template_name='mysite/login.html', context={"login_form":form})

def my_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('login')

def signup(request): 
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('login')
        messages.error(request, "Unsuccessful registration")
    else:
        form = SignUpForm()
    return render(request=request, template_name='mysite/signup.html', context={"signup_form":form})

def password_reset(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            assoc_users = User.objects.filter(Q(email=email))
            if assoc_users.exists():
                for user in assoc_users:
                    subject = "You requested a password reset - Barber Insitute"
                    email_template_name = 'mysite/email_template.txt'
                    c = {"email": user.email, "domain": '127.0.0.1:8000', "site_name": 'The Barber Insitute', "uid": urlsafe_base64_encode(force_bytes(user.pk)), "user":user, "token": default_token_generator.make_token(user), "protocol":"http",}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'barberinstitutetes@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_sent')
    form = PasswordResetForm()
    return render(request=request, template_name='mysite/forgotten_password.html', context={"password_reset_form":form})

def password_reset_sent(request):
    return render(request, 'mysite/password_reset_sent.html')

def password_reset_confirm(request):
    return render(request, 'mysite/password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'mysite/password_reset_complete.html')

def forbidden(request):
    return render(request, 'mysite/forbidden_page.html')

@login_required(login_url='forbidden')
def donate_fail(request):
    return render(request, 'mysite/donate_failed.html')

@login_required(login_url='forbidden')
def donate_success(request):
    return render(request, 'mysite/donate_success.html')

def create_donation(amount, image):
    donation_instance= Donation.objects.create(amount,image,User.first_name, User.last_name)