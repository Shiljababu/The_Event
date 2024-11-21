from django import forms
from adminpanel.models import Profile, Event, Ticket
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm



class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Name'
        })
    )
    email = forms.EmailField(
        label='email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password1 = forms.CharField(
        label='password1',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    password2 = forms.CharField(
        label='password2',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
   

    # Field for the phone number
    phone = forms.IntegerField(label='Phone Number', widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )

    # Field for the profile description (not required)
    profile_description = forms.CharField(label='Description', widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Say about you'
        }), 
        required=False
    )

    # Field for the email (not required)
    

    # Field for the profile image (not required)
    profile_image = forms.ImageField(label='Profile Image', widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your profile image'
        }), 
        required=False
    )

    # Field for the ID proof image (not required)
    id_proof = forms.ImageField(label='ID Proof', widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Upload your ID proof image'
        }), 
        required=False
    )

    # Connected to the Profile model and choose which fields to use
    class Meta:
        model = Profile
        fields = [ 'phone', 'profile_description', 'profile_image', 'id_proof']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class EventForm(forms.ModelForm):
    
    class Meta:
        model = Event
        fields = [
            'event_type', 'title', 'description', 'event_image', 'date', 
            'start_time', 'end_time', 'location', 'is_cancelled', 'venue', 
            'price_standard', 'price_premium', 'seats_available_standard', 'seats_available_premium'
        ]
        widgets = {
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter event description'}),
            'event_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'venue': forms.Select(attrs={'class': 'form-select'}),
            'price_standard': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter standard ticket price'}),
            'price_premium': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter premium ticket price'}),
            'seats_available_standard': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter standard ticket quantity'}),
            'seats_available_premium': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter premium ticket quantity'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['event', 'user', 'ticket_type', 'quantity_booked']
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
    
    class Meta:
        model = Profile
        fields = ['phone', 'profile_description', 'profile_image', 'id_proof']



class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']

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


class OtpForm(forms.Form):
     # Create a field for the OTP
    otp = forms.CharField(label='Enter OTP', max_length=6, min_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter 6-digit OTP'
    }))


class ResetForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    #fields to use in this form
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
