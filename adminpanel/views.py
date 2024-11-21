import logging
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from adminpanel.forms import AdminResetForm, LoginForm, VenueForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
# from adminpanel.tasks import send_activation_email_task, send_deactivation_email_task
from .models import BankAccount, Event, EventDeletionRequest, Interest, Notification, Review, Ticket, User, Profile, Venue
from django.contrib.auth import logout as auth_logout
from django.db import models
from django.shortcuts import get_object_or_404, redirect
from .models import Review, Event
logger = logging.getLogger(__name__)

# Create your views here.
def is_staff(user):
    return user.is_staff

@login_required(login_url='/404/')
@user_passes_test(is_staff)
# Function to handle user logout
def logout(request):
    # Log out the user.
    auth_logout(request)
    # Redirect to the home page after logging out.
    return redirect('siteadmin')


def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, 'you successfully logged in as a staff')
                return redirect('adminhome')
                
            else:
                messages.error(request, 'Invalid username or password or not authorized')
                return redirect('admin_login')
    else:
        form = LoginForm()

    return render(request, 'adminpanel/admin_login.html', {'form': form})


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def hide_event(request, event_type, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.status = 'hidden'  # Set event status to hidden
    event.save()
    message = f"Your event '{event.title}' has been hidden!"
    
    Notification.objects.create(user=event.organizer.user, message=message)
    messages.success(request, message)
    return redirect('adminhome')  # Redirect to admin home or other relevant page

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def show_event(request, event_type, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.status = 'visible'  # Set event status to visible
    event.save()
    message = f"Your event '{event.title}' has been visible now"
    Notification.objects.create(user=event.organizer.user, message=message)
    messages.success(request, message)
    return redirect('adminhome') 

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def adminhome(request):
    movies = Event.objects.filter(event_type='movie', status__in=['visible', 'hidden'])
    events = Event.objects.filter(event_type='event', status__in=['visible', 'hidden'])
    sports = Event.objects.filter(event_type='sport', status__in=['visible', 'hidden'])
    plays = Event.objects.filter(event_type='play', status__in=['visible', 'hidden'])
    activities = Event.objects.filter(event_type='activity', status__in=['visible', 'hidden'])

    context = {
        'event_categories': [
            ('Movies', movies),
            ('Events', events),
            ('Sports', sports),
            ('Plays', plays),
            ('Activities', activities)
        ]
    }
    return render(request, 'adminpanel/adminhome.html', context)



@login_required(login_url='/404/')
@user_passes_test(is_staff)
def movieslist(request):

    query = request.GET.get('q', '')
    
    visible_movies = Event.objects.filter(event_type='movie', status = 'visible')
    hidden_movies = Event.objects.filter(event_type='movie', status='hidden')
    
    if query:
        visible_movies = visible_movies.filter(title__icontains=query)
        hidden_movies = hidden_movies.filter(title__icontains=query)

    return render(request, 'adminpanel/movieslist.html', {
        'visible_movies': visible_movies,
        'hidden_movies': hidden_movies,
        'visible_count': visible_movies.count(),
        'hidden_count': hidden_movies.count(),
    })

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def event_list(request):

    query = request.GET.get('q', '')

    visible_events = Event.objects.filter(event_type='event', status = 'visible')
    hidden_events = Event.objects.filter(event_type='event', status='hidden')
    
    if query:
        visible_events = visible_events.filter(title__icontains=query)
        hidden_events = hidden_events.filter(title__icontains=query)

    return render(request, 'adminpanel/event_list.html', {
        'visible_events': visible_events,
        'hidden_events': hidden_events,
        'visible_count': visible_events.count(),
        'hidden_count': hidden_events.count(),
    })


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def sports_list(request):

    query = request.GET.get('q', '')

    visible_sports = Event.objects.filter(event_type='sport', status = 'visible')
    hidden_sports = Event.objects.filter(event_type='sport', status='hidden')
    
    if query:
        visible_sports = visible_sports.filter(title__icontains=query)
        hidden_sports = hidden_sports.filter(title__icontains=query)

    return render(request, 'adminpanel/sports_list.html', {
        'visible_sports': visible_sports,
        'hidden_sports': hidden_sports,
        'visible_count': visible_sports.count(),
        'hidden_count': hidden_sports.count(),
    })

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def plays_list(request):

    query = request.GET.get('q', '')

    visible_plays = Event.objects.filter(event_type='play', status = 'visible')
    hidden_plays = Event.objects.filter(event_type='play', status='hidden')
    
    if query:
        visible_plays = visible_plays.filter(title__icontains=query)
        hidden_plays = hidden_plays.filter(title__icontains=query)

    return render(request, 'adminpanel/sports_list.html', {
        'visible_plays': visible_plays,
        'hidden_plays': hidden_plays,
        'visible_count': visible_plays.count(),
        'hidden_count': hidden_plays.count(),
    })


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def activities_list(request):

    query = request.GET.get('q', '')

    visible_activities = Event.objects.filter(event_type='activity', status = 'visible')
    hidden_activities = Event.objects.filter(event_type='activity', status='hidden')
    
    if query:
        visible_activities = visible_activities.filter(title__icontains=query)
        hidden_activities = hidden_activities.filter(title__icontains=query)

    return render(request, 'adminpanel/activities_list.html', {
        'visible_activities': visible_activities,
        'hidden_activities': hidden_activities,
        'visible_count': visible_activities.count(),
        'hidden_count': hidden_activities.count(),
    })

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def approve_events(request):
    events = Event.objects.filter(is_approved=False)

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        event = Event.objects.get(id=event_id)
        event.is_approved = True
        
        event.save()
        organizer = event.organizer.user  # Assuming 'organizer' is a Profile model with a OneToOne relation to User

        message = f"Your event '{event.title}' has been approved!"
        
        # Create the notification for the organizer
        Notification.objects.create(user=event.organizer.user, message=message)
        messages.success(request, message)
        return redirect('approve_events')  # Refresh the page

    return render(request, 'adminpanel/approve_events.html', {
        'events': events
    })


from django.core.paginator import Paginator

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def admin_notification(request):
    # Ensure the current user is an admin
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")

    # Fetch notifications specifically assigned to the current admin user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # Paginate notifications
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render notifications in the admin panel template
    return render(request, 'adminpanel/admin_notification.html', {'page_obj': page_obj})





@login_required(login_url='/404/')
@user_passes_test(is_staff)
def event_deletion(request):
    # Ensure the user has staff privileges
    if not request.user.is_staff:
        return redirect('org_profile')  # Redirect non-staff users if necessary
    
    # Get all event deletion requests
    deletion_requests = EventDeletionRequest.objects.all().select_related('event', 'organizer')
    
    return render(request, 'adminpanel/event_deletion.html', {
        'deletion_requests': deletion_requests
    })

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def approve_event_deletion(request, request_id):
    # Ensure the user has staff privileges
    if not request.user.is_staff:
        return redirect('org_profile')  # Redirect non-staff users if necessary
    
    # Get the deletion request object
    deletion_request = get_object_or_404(EventDeletionRequest, id=request_id)
    
    # Approve the request by hiding the event
    event = deletion_request.event
    event.status = 'hidden'  # Set event status to 'hidden'
    event.save()

    Notification.objects.create(
        user=deletion_request.organizer,
        message=f"Your event '{event.title}' has been approved for deletion and is now hidden."
    )

    
    notify_users_on_event_cancellation(event)
    # Remove the deletion request after it's processed
    deletion_request.delete()
    
    messages.success(request, f"Event '{event.title}' has been hidden.")
    
    # Instead of redirecting, render the current page again
    return redirect('event_deletion_requests')  # The page will refresh with the updated state

@login_required(login_url='/404/')
@user_passes_test(is_staff)
def reject_event_deletion(request, request_id):
    # Ensure the user has staff privileges
    if not request.user.is_staff:
        return redirect('org_profile')  # Redirect non-staff users if necessary
    
    # Get the deletion request object
    deletion_request = get_object_or_404(EventDeletionRequest, id=request_id)
    

    Notification.objects.create(
        user=deletion_request.organizer,
        message=f"Your event deletion request for '{deletion_request.event.title}' has been rejected."
    )


    # Reject the request (delete it)
    deletion_request.delete()

    messages.warning(request, "The event deletion request has been rejected.")
    
    # Instead of redirecting, render the current page again
    return redirect('event_deletion_requests')




@login_required(login_url='/404/')
@user_passes_test(is_staff)
def userlist(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")

        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponseBadRequest("User not found")

            # Handle user activation/deactivation
            if action == "activate":
                user.is_active = True
                user.save()
                # Call the task to send a deactivation email to the user, passing their email and username
                # send_deactivation_email_task.delay(email=user.email, username=user.username, role="user")

                messages.success(request, f"{user.username} has been activated.")
            elif action == "deactivate":
                user.is_active = False
                user.save()
                # Call the task to send an activation email to the user, passing their email and username
                # send_activation_email_task.delay(email=user.email, username=user.username, role="user")

                messages.success(request, f"{user.username} has been deactivated.")
            
                # Optionally, update the user's bank account status when deactivating the user
                try:
                    bank_account = user.bankaccount
                    bank_account.status = 'inactive'  # Set to 'inactive' as an example
                    bank_account.save()
                except BankAccount.DoesNotExist:
                    pass  # Handle case where the bank account does not exist

            return redirect("userlist")  # Redirect to the user list page to refresh

    # Fetch normal users (excluding staff, superusers, and those with a different role)
    users = User.objects.filter(is_staff=False, is_superuser=False, profile__role='user')

    # Handle search functionality
    query = request.GET.get('q', '')
    if query:
        users = users.filter(username__icontains=query)

    # Categorize users based on their status
    active_users = users.filter(is_active=True)
    inactive_users = users.filter(is_active=False)

    return render(request, "adminpanel/userlist.html", {
        "users": users,
        "active_users": active_users,
        "inactive_users": inactive_users,
    })




@login_required(login_url='/404/')
@user_passes_test(is_staff)
def organizer_list(request):
    active_tab = request.POST.get("active_tab", "navs-pills-justified-home")  # Default to 'All Organizers' tab.

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")

        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return HttpResponseBadRequest("User not found")

            # Handle user activation/deactivation
            if action == "activate":
                user.is_active = True
                user.save()
                # send_activation_email_task.delay(email=user.email, username=user.username, role="organizer")
                messages.success(request, f"{user.username} has been activated.")
            elif action == "deactivate":
                user.is_active = False
                user.save()
                # send_deactivation_email_task.delay(email=user.email, username=user.username, role="organizer")
                messages.success(request, f"{user.username} has been deactivated.")

    # Fetch organizers based on the `role` in the Profile model
    organizers = Profile.objects.filter(role="organizer").select_related('user')

    # Handle search functionality
    query = request.GET.get('q', '')
    if query:
        organizers = organizers.filter(user__username__icontains=query)

    # Categorize organizers based on their active status
    active_organizers = organizers.filter(user__is_active=True)
    inactive_organizers = organizers.filter(user__is_active=False)
    context = {"organizers": organizers,
        "active_organizers": active_organizers,
        "inactive_organizers": inactive_organizers,
        "active_tab": active_tab,}
    return render(request, "adminpanel/organizer_list.html", context)


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def admin_reset_pass(request):
    # Create a form object to reset the password, with the current user's data
    form = AdminResetForm(user=request.user, data=request.POST or None)
    
    # If the form is submitted and the form data is correct
    if request.method == 'POST' and form.is_valid():
        # Save the new password for the user
        form.save()
        # Show a message that the password was updated successfully
        messages.success(request, 'Password updated successfully! Please log in again.')
        
        return redirect('admin_login')  
    
    return render(request, 'adminpanel/admin_reset_pass.html', {'form': form})



@login_required(login_url='/404/')
@user_passes_test(is_staff)
def admin_user_profile(request, user_id):
    # Get the user with the given ID or show a 404 page if not found.
    user = get_object_or_404(User, id=user_id)

    # Check if the form was submitted.
    if request.method == 'POST':
        # Get the action from the POST request.
        action = request.POST.get('action')
        
        # Check if the action is to activate the user.
        if action == 'activate':
            user.is_active = True  # Set the user's status to active.
            user.save()
            messages.success(request, f'User {user.username} activated.')
        
        # Check if the action is to deactivate the user.
        elif action == 'deactivate':
            user.is_active = False  # Set the user's status to inactive.
            user.save()
            messages.success(request, f'User {user.username} deactivated.')
        
        # Redirect to the user profile page after the action.
        return redirect('user_profile', user.id)

    # Get all events where the user is the organizer.
    events = Event.objects.filter(organizer=user.profile)

    # Determine if the user is an organizer (example using an 'organizer_profile' model)
    is_organizer = hasattr(user, 'organizer_profile')  # Assuming a one-to-one relation with an OrganizerProfile model

    # Render the user profile page with the user data.
    return render(request, 'adminpanel/admin_user_profile.html', {
        'user': user,
        'events': events,
        'is_organizer': is_organizer,
    })


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def admin_org_profile(request, organizer_id):
    organizer = get_object_or_404(Profile, id=organizer_id, role='organizer')
    events = Event.objects.filter(organizer=organizer)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deactivate':
            organizer.user.is_active = False
            organizer.user.save()
        elif action == 'activate':
            organizer.user.is_active = True
            organizer.user.save()
        return redirect('admin_org_profile', organizer_id=organizer.id)

    return render(request, 'adminpanel/admin_org_profile.html', {
        'organizer': organizer,
        'events': events,
    })



def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New venue is added")
            return redirect('view_venue')  
    else:
        form = VenueForm()

    return render(request, 'adminpanel/add_venue.html', {'form': form})


def view_venue(request):
    # Fetch all venue objects from the database
    venues = Venue.objects.all()
    
    # Pass the venues to the template
    return render(request, 'adminpanel/view_venue.html', {'venues': venues})

def edit_venue(request, id):
    venue = get_object_or_404(Venue, id=id)  # Get the venue to edit
    
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, " venue is edited")
            return redirect('view_venue')  # Redirect to the venues list after saving
    else:
        form = VenueForm(instance=venue)
    
    return render(request, 'adminpanel/edit_venue.html', {'form': form, 'venue': venue})


def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    venue.delete()
    messages.success(request, "Venue deleted successfully!")
    return redirect('view_venue') 


@login_required(login_url='/404/')
@user_passes_test(is_staff)
def view_each_event(request, event_id):
    logger.debug(f"View accessed for event ID: {event_id}")
    event = get_object_or_404(Event, id=event_id)
    reviews = Review.objects.filter(event=event)

    # Calculate total tickets booked for each type
    total_standard_tickets = Ticket.objects.filter(event=event, ticket_type='standard').aggregate(
        total_booked=models.Sum('quantity_booked'))['total_booked'] or 0
    total_premium_tickets = Ticket.objects.filter(event=event, ticket_type='premium').aggregate(
        total_booked=models.Sum('quantity_booked'))['total_booked'] or 0

    # Rating or interest count based on event type
    if event.event_type == 'movie':
        event_rating = reviews.filter(status='visible').aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        rated_users = reviews.filter(status='visible').values_list('user__username', flat=True)
    else:
        interest_count = Interest.objects.filter(event=event).count()
        interested_users = Interest.objects.filter(event=event).values_list('user__username', flat=True)
    
    # Handle review visibility toggle
    if request.method == 'POST':
        logger.debug(f"POST request data: {request.POST}")
        if 'toggle_review_status' in request.POST:
            review_id = request.POST.get('toggle_review_status')
            review = get_object_or_404(Review, id=review_id)
            review.status = 'hidden' if review.status == 'visible' else 'visible'
            review.save()
            messages.success(request, "review deleted successfully")
            return redirect('view_each_event', event_id=event_id)
    if 'toggle_event_status' in request.POST:
            event.status = 'hidden' if event.status == 'visible' else 'visible'
            event.save()
            logger.debug(f"Event status updated to: {event.status}")
            return redirect('view_each_event', event_id=event_id)

    context = {
        'events': Event.objects.all(),
        'event': event,
        'reviews': reviews,
        'event_rating': event_rating if event.event_type == 'movie' else None,
        'interest_count': interest_count if event.event_type != 'movie' else None,
        'total_standard_tickets': total_standard_tickets,
        'total_premium_tickets': total_premium_tickets,
        'rated_users': rated_users if event.event_type == 'movie' else None,
        'interested_users': interested_users if event.event_type != 'movie' else None,
    }
    return render(request, 'adminpanel/view_each_event.html', context)


def hide_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.status = 'hidden'
    review.save()
    return redirect('view_each_event', event_id=review.event.id)

def notify_users_on_event_cancellation(event):
    interested_users = Interest.objects.filter(event=event).select_related('user')
    for interest in interested_users:
        Notification.objects.create(
            user=interest.user,
            message=f"The event '{event.title}' has been canceled. We apologize for the inconvenience.",
        )