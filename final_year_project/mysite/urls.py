from django.urls import path
from mysite import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path('donate/', views.donate, name='donate'),
    path('events/', views.events, name='events'),
    path('donate_tiles/', views.donate_tiles, name='donate_tiles'),
    path('news/', views.news, name='news'),
    path('login/', views.login, name='login'),

] 
