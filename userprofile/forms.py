from django import forms
from django.contrib.auth.models import User


# Q1:forms对象到底是怎么回事?为什么能不调用MOdels?
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
