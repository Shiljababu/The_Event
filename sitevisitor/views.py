import random
from django.shortcuts import redirect, render
from django.contrib import messages
from adminpanel.models import Event, Profile, User
# from sitevisitor.tasks import send_otp_email_task, send_registration_email_task, send_verification_email_task
from .forms import LoginForm, OtpForm, ProfileForm, RegistrationForm, ResetForm, ForgotForm
from django.contrib.auth import authenticate, login
from datetime import datetime, timezone
from django.contrib.auth import get_user_model



def update_event_status():
    # Get all events that are currently visible or hidden
    events = Event.objects.filter(status__in=['visible', 'hidden'])
    today = datetime.now(timezone.utc).date()
    
    for event in events:
        # If the event date has passed, update its status to 'over'
        if event.date < today:
            event.status = 'draft'
            event.save()

def sitehome(request):
    update_event_status()
    context = {
        'events': {
            'Movie': Event.objects.filter(event_type='movie', is_approved = True, status = 'visible'),
            'Event': Event.objects.filter(event_type='event', is_approved = True, status = 'visible'),
            'Sport': Event.objects.filter(event_type='sport', is_approved = True, status = 'visible'),
            'Play': Event.objects.filter(event_type='play', is_approved = True, status = 'visible'),
            'Activities': Event.objects.filter(event_type='activity', is_approved = True, status = 'visible'),
        }
    }
    return render(request, 'sitevisitor/sitehome.html', context)




def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        is_organizer = request.POST.get('is_organizer') == 'on'  # Checkbox/radio button value

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data.get('email')
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
           
            login(request, user)
            messages.success(request, 'Successfully registered')
            return redirect('site_login')
        else:
            messages.error(request, 'Registration unsuccessful. Please correct the errors.')
    else:
        user_form = RegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'sitevisitor/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })





def site_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            # Check if the user is valid and meets criteria for 'user' role
            if user is not None:
                # Exclude superusers and staff, and only allow role 'user'
                if not user.is_staff and not user.is_superuser:
                    try:
                        profile = Profile.objects.get(user=user)
                    except Profile.DoesNotExist:
                        messages.error(request, 'Profile not found. Please register first.')
                        return redirect('register')

                    if profile.role == 'user':
                        print(f"Role of {user.username} is {profile.role}")
                        login(request, user)
                        return redirect('userhome')
                    else:
                        messages.error(request, 'Only regular users are allowed to log in here.')
                        return redirect('site_login')
                else:
                    messages.error(request, 'This user is not authorized.')
                    return redirect('site_login')
            else:
                messages.error(request, 'Invalid Username or Password!')
    else:
        form = LoginForm()

    return render(request, 'sitevisitor/site_login.html', {'form': form})

# This function handles OTP 
def site_otp(request):


#     # Check if the request method is POST
    if request.method == 'POST':


#         # Create a form with the data from the POST request
        form = OtpForm(request.POST)


#         # Check if the form is valid
        if form.is_valid():


#             # Get the entered OTP from the form
            # entered_otp = form.cleaned_data.get('otp')


#             # Get the OTP stored in the session
            # session_otp = request.session.get('otp_code')


#             # Get the email address from the session
            # email = request.session.get('email')
       
#             # Get the time when the OTP was created from the session
            # otp_created_at = request.session.get('otp_created_at')
            
#             # Check if there is an OTP and its creation time in the session
            # if session_otp and otp_created_at:


#                 # Convert the creation time from the session to a datetime object
                # otp_creation_time=datetime.fromisoformat(otp_created_at)
                
#                 # Get the current time
                # current_time = datetime.now()


#                 # Calculate the difference in minutes between the current time and OTP creation time
                # time_diff = (current_time - otp_creation_time).total_seconds() / 60  
            
#             # Check if the time difference is greater than 5 minutes 
            # if time_diff > 5:


#                 # Show an error message that the OTP has expired
                messages.error(request, 'OTP expired. Please request a new OTP.')
#                 # Redirect the user back to the OTP page
                return redirect('site_otp')


#             # Check if the entered OTP matches the session OTP
            # if entered_otp == session_otp:


#                 # Show a success message that the OTP is verified
                messages.success(request, 'OTP verified successfully!')


#                 # Send a confirmation email after the OTP is verified
                # send_verification_email_task.delay(email)


#                 # Remove the OTP from the session to prevent reuse
                # request.session.pop('otp', None) 


#                 # Redirect the user to the reset password page
                return redirect('reset')


        else:
#                 # Show an error message if the OTP is invalid
                messages.error(request, 'Invalid OTP. Please try again.')


#                 # Redirect the user back to the OTP page
                return redirect('site_otp')


    else:
#         # If the request is not a POST, create a new empty form
        form = OtpForm()
    
#     # Render the OTP page with the form
    return render(request, 'sitevisitor/site_otp.html', {'form': form})


# def site_otp(request):
#     # Check if the request method is POST, meaning the form has been submitted
#     if request.method == 'POST':
#         # Create a form with the data from the POST request
#         form = OtpForm(request.POST)

#         # Check if the form is valid
#         if form.is_valid():
#             # Get the entered OTP from the form
#             entered_otp = form.cleaned_data.get('otp')

#             # Get the OTP stored in the session
#             session_otp = request.session.get('otp')

#             # Get the email address from the session
#             email = request.session.get('email')
	   
#             # Get the time when the OTP was created from the session
#             otp_created_at = request.session.get('otp_created_at')
            
#             # Check if there is an OTP and its creation time in the session
#             if session_otp and otp_created_at:
#                 # Convert the creation time from the session to a datetime object
#                 otp_creation_time = datetime.datetime.fromisoformat(otp_created_at)
                
#                 # Get the current time
#                 current_time = datetime.datetime.now()

#                 # Calculate the difference in minutes between the current time and OTP creation time
#                 time_diff = (current_time - otp_creation_time).total_seconds() / 60  
            
#             # Check if the time difference is greater than 5 minutes (or 1 minute in your code)
#             if time_diff > 5:
#                 # Show an error message that the OTP has expired
#                 messages.error(request, 'OTP expired. Please request a new OTP.')
#                 # Redirect the user back to the OTP page
#                 return redirect('site_otp')

#             # Check if the entered OTP matches the session OTP
#             if entered_otp == session_otp:
#                 # Show a success message that the OTP is verified
#                 messages.success(request, 'OTP verified successfully!')

#                 # Redirect the user to the reset password page
#                 return redirect('reset')

#             else:
#                 # Show an error message if the OTP is invalid
#                 messages.error(request, 'Invalid OTP. Please try again.')

#                 # Redirect the user back to the OTP page
#                 return redirect('site_otp')

#     else:
#         # If the request is not a POST, create a new empty form
#         form = OtpForm()
    
#     # Render the OTP page with the form
#     return render(request, 'sitevisitor/site_otp.html', {'form': form})





def forgot(request):
    # Check if the user has submitted the forgot password form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = ForgotForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the email from the form.
            email = form.cleaned_data.get('email')
            # Check if a user with that email exists.
            if User.objects.filter(email=email).exists():
                # Generate a 6-digit OTP
                # otp_code = ''.join(random.choices('0123456789', k=6))
                # Send the OTP to the user's email using Celery task
                # send_otp_email_task.delay(email, otp_code)
                # Show a success message if the email is found.
                messages.success(request, 'Instructions to reset your password has been sent to your email')
               # Store the generated OTP in the session
                # request.session['otp_code'] = otp_code  


                # Store the user's email in the session 
                # request.session['email'] = email  


		 # Store the current time as string
                # request.session['otp_created_at']=str(datetime.now())  



                # Send the user to the reset page.
                return redirect('site_otp')
            else:
                # Show an error if the email is not found.
                messages.error(request, 'This email id does not exist!!!')
                # Stay on the forgot password page.
                return redirect('forgot')
    else:
        # If it’s not a POST request, show the forgot password form.
        form = ForgotForm()
    # Show the 'forgot_pass.html' page with the form.
    return render(request, 'sitevisitor/forgot.html', {'form':form})




def reset(request):
    # Check if the user has submitted the reset password form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = ResetForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the username and new passwords from the form.
            username = form.cleaned_data.get('username')
            new_password3 = form.cleaned_data.get('password3')
            new_password4 = form.cleaned_data.get('password4')

            # Check if the new passwords match.
            if new_password3 != new_password4:
                # Show an error if the passwords don't match.
                form.add_error('password4', 'Passwords do not match.')
            else:
                # Find the user and set the new password.
                user = User.objects.filter(username=username).first()
                if user:
                    user.set_password(new_password3)
                    user.save()
                    # Show a success message.
                    messages.success(request, 'Your password has been updated successfully.')
                    # Send the user to the login page.
                    return redirect('site_login')
                else:
                    # Show an error if the user is not found.
                    form.add_error('username', 'User does not exist.')
        else:
            # Show an error if the form has mistakes.
            messages.error(request, 'Please correct the errors.')
    else:
        # If it’s not a POST request, show the reset form.
        form = ResetForm()
    # Show the 'reset.html' page with the form.
    return render(request, 'sitevisitor/reset.html', {'form': form})



def org_reset(request):
    # If the request is POST (form submission)
    if request.method == 'POST':
        form = ResetForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            username = form.cleaned_data['username']
            password3 = form.cleaned_data['password3']
            password4 = form.cleaned_data['password4']

            # Check if the passwords match
            if password3 != password4:
                form.add_error('password4', 'Passwords do not match.')
            else:
                # Attempt to find the user by username
                try:
                    user = get_user_model().objects.get(username=username)
                    # If user is found, reset password
                    user.set_password(password3)
                    user.save()
                    messages.success(request, 'Your password has been updated successfully.')
                    return redirect('site_login')  # Redirect to login page after success
                except get_user_model().DoesNotExist:
                    form.add_error('username', 'User with this username does not exist.')
        else:
            messages.error(request, 'Please correct the errors in the form.')

    else:
        form = ResetForm()  # Show the reset form if it's not a POST request

    # Render the reset password template with the form
    return render(request, 'sitevisitor/org_reset.html', {'form': form})



def error_page(request):
    # Show the '404.html' error page.
    return render(request, 'sitevisitor/404.html')


