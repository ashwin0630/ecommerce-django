from django.contrib.auth.forms import UserCreationForm
from .models import User,product
from django import forms

class customuserform(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter username'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter emailid'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'enter confirm password'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class sellerform(forms.ModelForm):
    class Meta:
        model=product
        exclude = ('status','trending','created_at')
