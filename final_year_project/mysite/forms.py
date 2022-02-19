from django import forms
from .models import User
from .models import Image
from .models import Comment
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
    
class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = ['fave_img']

