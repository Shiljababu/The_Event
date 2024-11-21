import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from adminpanel.models import Profile


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your name'
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm your password'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
  

class ProfileForm(forms.ModelForm):
    phone = forms.IntegerField(label='Phone Number', widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your phone number'
    }))
    profile_description = forms.CharField(label='Description', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Say something about you'
    }), required=False)
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }), required=False)
    id_proof = forms.ImageField(label='ID Proof', widget=forms.ClearableFileInput(attrs={
        'class': 'form-control'
    }), required=False)
    is_active = forms.BooleanField(initial=True, required=False)  # Add default value
    is_organizer = forms.BooleanField(required=False)  # Set based on user type in view

    class Meta:
        model = Profile
        fields = ['phone', 'profile_description', 'profile_image', 'id_proof', 'is_active', 'is_organizer']


class LoginForm(forms.Form):
    # Create a field for the username
    username = forms.CharField(label = 'Username', max_length = 100, required = True, widget = forms.TextInput(attrs = {
        'class':'form-control', 'placeholder':'Enter the username or email'
    }))

    # Create a field for the password
    password = forms.CharField(label = 'password', max_length = 100, required =True, widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':'Enter the password'
    }))

    # Tell the form which model it should use.
    class Meta:
        model = User
        # Include these fields in the form
        fields = ['username','email','password']


class OtpForm(forms.Form):
     # Create a field for the OTP
    otp = forms.CharField(label='Enter OTP', max_length=6, min_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter 6-digit OTP'
    }))


class ForgotForm(forms.Form):  # Use forms.Form instead of forms.ModelForm since it's not tied to a model
    email = forms.EmailField(
        label='Email', max_length=100, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Enter the Email address'
        })
    )
    
    # Tell the form which model it should use.
    class Meta:
        model = User
        # Include the email field in the form.
        fields = ['email']


class ResetForm(forms.Form):
    # Create a field for the username
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))

    # Create a field for the password 1
    password3 = forms.CharField(label='password3',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your new password'
        }))
    
    # Create a field for the password2
    password4 = forms.CharField(label='password4',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm your password'
        }))
    
   
    class Meta:
         # Include these fields in the form.
        fields = ['username','password3', 'password4']


