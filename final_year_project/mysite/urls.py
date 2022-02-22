from django.urls import path,include
from mysite import views
from django.contrib import admin
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('', views.my_login, name="login"),
    path('donate/', views.donate, name='donate'),
    path('events/', views.events, name='events'),
    path('donate_tiles/', views.donate_tiles, name='donate_tiles'),
    path('news/', views.news, name='news'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.my_logout, name="logout"),
    path('forgotpassword/', views.password_reset, name="forgotten_password"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="mysite/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='mysite/password_reset_sent.html'), name="password_reset_sent"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='mysite/password_reset_complete.html'), name="password_reset_complete"),
    path('forbidden/', views.forbidden, name="forbidden"),
    path('donate_failed/', views.donate_fail, name="donate_fail"),
    path('donate_success/', views.donate_success, name="donate_success"),
    path('donate_history/', views.donate_history, name="donate_history"),
    path('liked_posts/', views.liked_posts, name="liked_posts"),
  

] 
