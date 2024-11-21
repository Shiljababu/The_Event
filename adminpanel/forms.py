from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Venue

class LoginForm(forms.Form):
    # Create a field for the username
    username = forms.CharField(label = 'Username', max_length = 100, required = True, widget = forms.TextInput(attrs = {
        'class':'form-control', 'placeholder':'Enter the username'
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



# Form for changing user passwords
class AdminResetForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    #fields to use in this form
    class Meta:
        fields = ['old_password1', 'new_password3', 'new_password4']


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'description', 'venue_image']  # Fields to include in the form

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

