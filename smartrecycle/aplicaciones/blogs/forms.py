from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
        
class PostCommentForm(forms.ModelForm):
    content = forms.CharField(label='Ingrese su comentario')
    
    class Meta:
        model = Comment
        fields = ['content']