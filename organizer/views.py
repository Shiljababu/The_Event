
from datetime import datetime
import random
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from adminpanel.models import Event, EventDeletionRequest, Interest, Notification, Profile, Review, Ticket, User
from django.contrib.auth import login
# from .tasks import send_otp_email_task, send_registration_email_task, send_verification_email_task
from .forms import EventForm, ForgotForm, LoginForm, OtpForm, ProfileForm, RegistrationForm, ResetForm, TicketForm, UserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db import models
from django.contrib.auth import logout as auth_logout
# Create your views here.

def is_organizer(user):
    return hasattr(user, 'profile') and user.profile.role == 'organizer'

def org_register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data.get('email')
            user.save()
            # Send email using Celery
            # send_registration_email_task.delay(user.email, user.username)
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = 'organizer'  # Set role to 'organizer'
            profile.save()

            login(request, user)
            messages.success(request, 'Successfully registered as an organizer!')
            return redirect('org_home')
        else:
            messages.error(request, 'Registration unsuccessful. Please check the form fields for errors.')
    else:
        user_form = RegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'organizer/org_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def org_login(request):
    if request.method == 'POST':
        print("POST request received")
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            print("Form is valid")
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_superuser:
                if hasattr(user, 'profile') and user.profile.role == 'organizer':
                    login(request, user)
                    print(f"User '{user.username}' has logged in successfully.")
                    messages.success(request, 'Successfully logged in as an organizer!')
                    return redirect('org_home')
                else:
                    messages.error(request, 'You are not authorized to log in as an organizer.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            print("Form is not valid")
    else:
        login_form = LoginForm()

    return render(request, 'organizer/org_login.html', {
        'login_form': login_form
    })


@login_required(login_url='/404/')  # Ensures only logged-in users can access this view
def org_reset_pass(request):
    # Ensure the form is initialized with the current logged-in user
    if request.method == 'POST':  
        # Create form with submitted data and current user (the logged-in organizer)
        form = ResetForm(user=request.user, data=request.POST) 
        
        # Check if the form data is valid 
        if form.is_valid(): 
            # Save the new password to the database
            form.save()  
            
            # Show success message
            messages.success(request, 'Your password has been updated successfully.')
            
            # Redirect to the login page for re-authentication
            return redirect('org_login')  
        else:
            # Show error message if the form is not valid
            messages.error(request, 'Please correct the errors below.')
    else:
        # If not a POST request, initialize the form with the current user
        form = ResetForm(user=request.user) 
    
    return render(request, 'organizer/org_reset_pass.html', {'form': form})


@login_required(login_url='/404/')
def edit_org_profile(request):
    user = request.user  # Get the logged-in user
    profile = user.profile  # Assume OneToOne relationship between User and Profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Update the User model
            profile_form.save()  # Update the Profile model
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('org_home')  # Redirect to a success page (e.g., organizer home)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'organizer/edit_org_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def update_event_status():
    # Get all events that are still visible or hidden
    events = Event.objects.filter(status__in=['visible', 'hidden'])
    today = timezone.now().date()
    
    for event in events:
        # If the event date has passed, update its status to 'draft'
        if event.date < today:
            event.status = 'draft'
            event.save()



@login_required(login_url='/404/')
def org_home(request):
    update_event_status()
    events = Event.objects.filter(organizer=request.user.profile, status='visible').order_by('-date') 
    return render(request, 'organizer/org_home.html', {'events': events} )


@login_required(login_url='/404/')
def drafts(request):
    update_event_status()
    events = Event.objects.filter(organizer=request.user.profile, status='draft').order_by('-date') 
    return render(request, 'organizer/drafts.html', {'events': events} )




@login_required(login_url='/404/')
def contact_form(request, event_id):
    # Ensure the logged-in user has the organizer role
    profile = get_object_or_404(Profile, user=request.user, role='organizer')

    # Get the event associated with the organizer
    event = get_object_or_404(Event, id=event_id, organizer=profile, status='visible')

    if request.method == "POST":
        # Get the reason from the form
        reason = request.POST.get('reason', '').strip()
        if reason:
            # Create a deletion request
            EventDeletionRequest.objects.create(
                organizer=request.user,
                event=event,
                reason=reason,
            )

            admin_users = User.objects.filter(is_staff=True)  # Assuming you have an 'Admin' group
            for admin in admin_users:
                message = f"Organizer {request.user.username} has submitted a deletion request for event '{event.title}'."
                Notification.objects.create(user=admin, message=message)
                messages.success(request, f"Organizer {request.user.username} has submitted a deletion request for event '{event.title}'.")


            # Redirect to the organizer's profile after submission
            return redirect('org_profile')

    # Render the contact form with event details for GET requests
    return render(request, 'organizer/contact_form.html', {'event': event})


@login_required(login_url='/404/')
def delete_event(request, event_id):
    # Ensure the logged-in user has a profile with organizer role
    profile = get_object_or_404(Profile, user=request.user, role='organizer')

    # Fetch the hidden event created by the organizer
    event = get_object_or_404(Event, id=event_id, organizer=profile, status='hidden')

    if request.method == "POST":
        # Allow direct deletion of hidden events
        event.delete()
        return redirect('org_profile')  # Redirect back to the organizer's profile
    messages.success(request, "The event is deleted successfully")
    # Render a confirmation page for GET requests
    return render(request, 'userpanel/delete_event.html', {'event': event})



@login_required(login_url='/404/')
def org_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
        published_events = None
    
    else:
        # Filter events by visibility
        published_events = Event.objects.filter(organizer=profile, status = 'visible')
        

    return render(
        request, 
        'organizer/org_profile.html', 
        {'profile': profile, 'published_events': published_events}
    )


@login_required(login_url='/404/')
def hidden_events(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None
        hidden_events = None
    else:
        hidden_events = Event.objects.filter(organizer=profile, status = 'hidden')

    return render(
        request, 
        'organizer/hidden_events.html', 
        {'profile': profile, 'hidden_events': hidden_events}
    )

@login_required(login_url='/404/')
def add_event(request):
    event_form = EventForm(request.POST or None, request.FILES or None)

    # Ensure the profile associated with the logged-in user has the 'organizer' role
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={'role': 'organizer'})

    if profile.role != 'organizer':
        # Redirect or show an error if the logged-in user is not an organizer
        return redirect('error_page')  
    
    message = "" 

    if request.method == 'POST' and event_form.is_valid():
        
        # Save the event with the organizer's profile
        event = event_form.save(commit=False)
        event.is_approved = False
        event.organizer = profile
        event.save()
        messages.success(request, "A new event is added successfully")
        # Create default tickets for the event
        Ticket.objects.create(
            event=event, 
            user=request.user,  
            ticket_type='standard',  
            quantity_booked=0,  
            status='pending'  
        )
        Ticket.objects.create(
            event=event, 
            user=request.user,
            ticket_type='premium',  
            quantity_booked=0,  
            status='pending'  
        )

        admins = User.objects.filter(is_staff=True)  # Get all admin users
        for admin in admins:
            message = f"New event '{event.title}' has been added by organizer {request.user.username}."
            Notification.objects.create(user=admin, message="A new event has been added by the organizer." )
            
        return redirect('org_home')  # Redirect to organizer's home if successful

    # Render the form templates
    return render(request, 'organizer/add_event.html', {
        'event_form': event_form,
        'profile': profile,
        'message':message,  # Pass profile to access the organizer's name in the template
    })



@login_required(login_url='/404/')
@user_passes_test(is_organizer)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_type = event.event_type
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES, instance=event)
        if event_form.is_valid():
            event_form.save()
            notify_users_on_event_update(event)
            messages.success(request, 'Event updated successfully.')
            
            return redirect('org_view_event', event_type=event_type, event_id=event.id)  # Replace 'event_detail' with your event detail view name
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        event_form = EventForm(instance=event)

    return render(request, 'organizer/edit_event.html', {'event_form': event_form, 'event': event})


@login_required(login_url='/404/')
def notification(request):
    # Updated to fetch notifications using 'user'
    notifications = request.user.notifications.order_by('-created_at')
    notifications.update(is_read=True)  # Mark all notifications as read
    return render(request, 'organizer/notification.html', {'notifications': notifications})



def get_interested_count(event):
    return Interest.objects.filter(event=event).count()



@login_required(login_url='/404/')
def org_view_event(request, event_type, event_id):
    print(f"Event Type: {event_type}, Event ID: {event_id}")
    event_type = event_type.lower()

    if event_type not in ['movie', 'event', 'sport', 'play', 'activity']:
        return HttpResponse("Invalid event type.", status=400)

    # Fetch the event object
    event = get_object_or_404(Event, id=event_id, event_type=event_type)

    
    # Rating or interest count based on event type
    reviews = None
    if event.event_type == 'movie':
        reviews = Review.objects.filter(event=event, status='visible')
        user_ratings = {review.user.id: review.rating for review in reviews}
        event_rating = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
    # Fetch count of interests and check if the current user is interested
    interests_count = Interest.objects.filter(event=event).count()
    is_interested = Interest.objects.filter(event=event, user=request.user).exists()
    
    # Count of users booked for tickets
    standard_ticket_count = Ticket.objects.filter(event=event, ticket_type='standard').count()
    premium_ticket_count = Ticket.objects.filter(event=event, ticket_type='premium').count()
    filled_stars = int(event_rating)
    empty_stars = 5 - filled_stars
    filled_star_range = range(filled_stars)
    empty_star_range = range(empty_stars)

    context = {
        'event': event,
        'standard_ticket_count': standard_ticket_count,
        'premium_ticket_count': premium_ticket_count,
        'reviews': reviews,
        'interests_count': interests_count,
        'is_interested': is_interested,
        'event_rating': event_rating if event.event_type == 'movie' else None,
        'empty_stars': empty_stars,
        'filled_stars': filled_stars,
        'filled_star_range': filled_star_range,
        'empty_star_range': empty_star_range,
        'user_ratings':user_ratings,
    }

    return render(request, 'organizer/org_view_event.html', context)


@login_required(login_url='/404/')
def org_forgot(request):
    # Check if the user has submitted the forgot password form.
    if request.method == 'POST':
        # Create a form with the submitted data.
        form = ForgotForm(request.POST)
        # Check if the form data is correct.
        if form.is_valid():
            # Get the email from the form.
            email = form.cleaned_data.get('email')
            # Check if an organizer with that email exists.
            if Profile.objects.filter(user__email=email, role='organizer').exists():
                # Generate a 6-digit OTP
                # otp_code = ''.join(random.choices('0123456789', k=6))
                # Send the OTP to the organizer's email using Celery task
                # send_otp_email_task.delay(email, otp_code)
                # Show a success message if the email is found.
                messages.success(request, 'Instructions to reset your password have been sent to your email.')
                # Store the generated OTP in the session
                # request.session['otp_code'] = otp_code
                # Store the organizer's email in the session
                # request.session['email'] = email
                # Store the current time as a string
                # request.session['otp_created_at'] = str(datetime.now())
                # Redirect the user to the OTP verification page
                return redirect('org_otp')
            else:
                # Show an error if the email is not found or not an organizer
                messages.error(request, 'This email does not belong to an organizer account!')
                # Stay on the forgot password page
                return redirect('org_forgot')
    else:
        # If it’s not a POST request, show the forgot password form.
        form = ForgotForm()
    # Show the 'forgot_pass.html' page with the form.
    return render(request, 'organizer/org_forgot.html', {'form': form})


@login_required(login_url='/404/')
def org_otp(request):


    # Check if the request method is POST
    if request.method == 'POST':


        # Create a form with the data from the POST request
        form = OtpForm(request.POST)


        # Check if the form is valid
        if form.is_valid():


            # Get the entered OTP from the form
            # entered_otp = form.cleaned_data.get('otp')


            # Get the OTP stored in the session
            # session_otp = request.session.get('otp_code')


            # Get the email address from the session
            # email = request.session.get('email')
       
            # Get the time when the OTP was created from the session
            # otp_created_at = request.session.get('otp_created_at')
            
            # Check if there is an OTP and its creation time in the session
            # if session_otp and otp_created_at:


                # Convert the creation time from the session to a datetime object
                # otp_creation_time=datetime.fromisoformat(otp_created_at)
                
                # Get the current time
                # current_time = datetime.now()


                # Calculate the difference in minutes between the current time and OTP creation time
                # time_diff = (current_time - otp_creation_time).total_seconds() / 60  
            
            # Check if the time difference is greater than 5 minutes 
            # if time_diff > 5:


                # Show an error message that the OTP has expired
                messages.error(request, 'OTP expired. Please request a new OTP.')
                # Redirect the user back to the OTP page
                return redirect('org_otp')


            # Check if the entered OTP matches the session OTP
            # if entered_otp == session_otp:


                # Show a success message that the OTP is verified
                messages.success(request, 'OTP verified successfully!')


                # Send a confirmation email after the OTP is verified
                # send_verification_email_task.delay(email)


                # Remove the OTP from the session to prevent reuse
                # request.session.pop('otp', None) 


                # Redirect the user to the reset password page
                return redirect('org_reset_pass')


        else:
                # Show an error message if the OTP is invalid
                messages.error(request, 'Invalid OTP. Please try again.')


                # Redirect the user back to the OTP page
                return redirect('org_otp')


    else:
        # If the request is not a POST, create a new empty form
        form = OtpForm()
    
    # Render the OTP page with the form
    return render(request, 'organizer/org_otp.html', {'form': form})


def notify_users_on_event_update(event):
    interested_users = Interest.objects.filter(event=event).select_related('user')
    print(f"Found {interested_users.count()} users interested in event: {event.title}")  # Log the count

    for interest in interested_users:
        print(f"Notifying user: {interest.user.username}")  # Log each user
        Notification.objects.create(
            user=interest.user,
            message=f"The event '{event.title}' has been updated. Check the latest details.",
        )



@login_required(login_url='/404/')
def logout(request):
    auth_logout(request)
    # Redirect to the home page after logging out
    return redirect('sitehome')
