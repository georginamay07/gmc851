from django.urls import path
from mysite import views

urlpatterns = [
    path("", views.login, name="login"),
    path('donate/', views.donate, name='donate'),
    path('events/', views.events, name='events'),
    path('donate_tiles/', views.donate_tiles, name='donate_tiles'),
    path('news/', views.news, name='news'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name="signup"),
    

] 
