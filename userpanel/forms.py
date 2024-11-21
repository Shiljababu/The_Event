
from django import forms
from django.contrib.auth.models import User
from adminpanel.models import Profile, Review
from django.contrib.auth.forms import PasswordChangeForm

class TicketSelectionForm(forms.Form):
    TICKET_CHOICES = [
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]
    
    ticket_type = forms.ChoiceField(choices=TICKET_CHOICES, widget=forms.HiddenInput())
    seat_count = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
    


class AccountCheckForm(forms.Form):
    
    username = forms.CharField(label = "Username")
    
    card_number = forms.CharField(label="Card Number", max_length=16, min_length=10)
    card_expiry_date = forms.CharField(label="Card Expiry Date", max_length=5, help_text="Format: MM/YY")
    cvv = forms.CharField(label="CVV", max_length=3, min_length=3, widget=forms.PasswordInput)


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


class ResetForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    #fields to use in this form
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']




class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here...'}),
            'rating': forms.HiddenInput(),  # Use a hidden input for the star rating
        }

    # Optional: Add custom validation if needed
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not (1 <= rating <= 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating

