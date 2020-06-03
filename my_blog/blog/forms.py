from django import forms
from .models import Post,Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    text = forms.CharField(widget = forms.Textarea)


    class Meta():
        model = Post
        fields = ('title','text')









class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta():
        model = User
        fields = ('username','password')

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ('author','text')
