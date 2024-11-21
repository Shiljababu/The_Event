from datetime import date, datetime, timedelta
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from adminpanel.models import BankAccount, Event, Interest, Notification, Profile, Review, ReviewLikeDislike, Ticket, Venue, User
from django.contrib import messages
from django.http import HttpResponse
from .forms import AccountCheckForm, ResetForm, ReviewForm, TicketSelectionForm
from django.shortcuts import render
from django.utils import timezone
from .forms import UserForm, ProfileForm
from django.utils import timezone
from django.db.models import Avg, Count
from django.contrib.auth import logout as auth_logout


def update_event_status():
    # Get all events that are currently visible or hidden
    events = Event.objects.filter(status__in=['visible', 'hidden'])
    today = timezone.now().date()
    
    for event in events:
        # If the event date has passed, update its status to 'over'
        if event.date < today:
            event.status = 'draft'
            event.save()



@login_required(login_url='/404/')
def userhome(request):
    # Update event status based on event dates
    update_event_status()

    # Get events by category
    events = {
        'Movie': Event.objects.filter(event_type='movie', is_approved=True, status='visible'),
        'Event': Event.objects.filter(event_type='event', is_approved=True, status='visible'),
        'Sport': Event.objects.filter(event_type='sport', is_approved=True, status='visible'),
        'Play': Event.objects.filter(event_type='play', is_approved=True, status='visible'),
        'Activit': Event.objects.filter(event_type='activity', is_approved=True, status='visible'),
    }

    for category, items in events.items():
        for item in items:
            # Get the average rating for each event
            average_rating = Review.objects.filter(event=item).aggregate(Avg('rating'))['rating__avg']
            # If no reviews exist, set the rating to 0
            item.average_rating = average_rating if average_rating is not None else 0
            
            # Calculate filled and empty stars
            item.filled_stars = range(int(item.average_rating))  # Filled stars based on average rating
            item.empty_stars = range(int(item.average_rating), 5)  # Empty stars to complete 5 stars

    context = {
        'events': events,
    }

    return render(request, 'userpanel/userhome.html', context)


@login_required(login_url='/404/')
def movies(request):
    update_event_status()
    
    # Fetch movies
    movies = Event.objects.filter(event_type='movie')
    
    for movie in movies:
        # Calculate the average rating
        average_rating = Review.objects.filter(event=movie).aggregate(Avg('rating'))['rating__avg']
        movie.average_rating = average_rating if average_rating is not None else 0

        # Calculate filled and empty stars
        movie.filled_stars = range(int(movie.average_rating))  # Filled stars
        movie.empty_stars = range(int(movie.average_rating), 5)  # Empty stars to complete 5 stars

    return render(request, 'userpanel/movies.html', {'movies': movies})


@login_required(login_url='/404/')
def events(request):
    update_event_status()
    events = Event.objects.filter(event_type='event', status='visible')
    return render(request, 'userpanel/conference.html', {'events':events})


@login_required(login_url='/404/')
def activities(request):
    update_event_status()
    activities = Event.objects.filter(event_type='activity', status='visible')
    return render(request, 'userpanel/activities.html', {'activities':activities})


@login_required(login_url='/404/')
def sports(request):
    update_event_status()
    sports = Event.objects.filter(event_type='sport', status='visible')
    return render(request, 'userpanel/sports.html', {'sports':sports})


@login_required(login_url='/404/')
def plays(request):
    update_event_status()
    plays = Event.objects.filter(event_type='play', status='visible')
    return render(request, 'userpanel/plays.html', {'plays':plays})


@login_required(login_url='/404/')
def ticket(request):
    return render(request, 'userpanel/ticket.html')




@login_required(login_url='/404/')
def get_interested_count(event):
    return Interest.objects.filter(event=event).count()



@login_required(login_url='/404/')
def view_event(request, event_type, event_id):
    print(f"Event Type: {event_type}, Event ID: {event_id}") 
    event_type = event_type.lower()

    if event_type not in ['movie', 'event', 'sport', 'play', 'activity']:
        return HttpResponse("Invalid event type.", status=400)
 # Debu
    # Fetch the event object and the existing ticket associated with this event
    event = get_object_or_404(Event, id=event_id, event_type = event_type)
    ticket = Ticket.objects.filter(event=event).first()  # Assume one ticket per event
    reviews = Review.objects.filter(event=event, status =  'visible') if event.event_type == 'movie' else None
    interests = Interest.objects.filter(event=event).count()
    is_interested = Interest.objects.filter(event=event, user=request.user).exists()
   
    interests_count = get_interested_count(event)

    if not ticket:
        return HttpResponse("No tickets available for this event.", status=404)

    if request.method == 'POST':
        form = TicketSelectionForm(request.POST)
        if form.is_valid():
            # Retrieve the cleaned data from the form
            ticket_type = form.cleaned_data['ticket_type']
            seat_count = form.cleaned_data['seat_count']

            # Determine ticket price and calculate the total amount
            ticket_price = event.price_premium if ticket_type == 'premium' else event.price_standard
            total_amount = (ticket_price * seat_count) + 10  # Adding service charge

            # Update the existing ticket with the booking details
            ticket.ticket_type = ticket_type
            ticket.quantity_booked = seat_count
            ticket.total_amount = total_amount
            ticket.status = 'pending'  # Set status to pending on booking
            ticket.save()

            # Redirect to payment page with ticket details
            return redirect('payment_page', event_type=event_type, event_id=event.id)
        else:
            # Display form errors for troubleshooting
            print("Form errors:", form.errors)
            context['form_errors'] = form.errors
            return HttpResponse("Form submission failed due to errors.", status=400)

    else:
        # Initialize the form with the existing ticket details
        form = TicketSelectionForm(initial={
            'ticket_type': ticket.ticket_type or 'standard',  # Default to 'standard' if empty
            'seat_count': ticket.quantity_booked or 1  # Default to 1 if empty
        })
    
    # Calculate remaining tickets for each type
    available_standard_tickets = event.seats_available_standard - ticket.quantity_booked
    available_premium_tickets = event.seats_available_premium - ticket.quantity_booked

    context = {
        'event': event,
        'day_event': [event],
        'premium_price': event.price_premium,
        'standard_price': event.price_standard,
        'quantity_available_standard': available_standard_tickets,  # Updated to show available tickets
        'quantity_available_premium': available_premium_tickets,  # Updated to show available tickets
        'venue': getattr(event, 'venue', None),
        'event_id': event.id,
        'form': form,
        'reviews': reviews,
        'interests_count': interests,
        'is_interested': is_interested,
        'selected_ticket_type': ticket.ticket_type,  # Displayed if ticket exists
        'selected_seat_count': ticket.quantity_booked,
        'interests_count': interests_count,  # Add interest count here
        'is_interested': is_interested,
        'range': range(1, 6),
    }

    return render(request, 'userpanel/view_event.html', context)


@login_required(login_url='/404/')
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Calculate total price based on ticket type
    if ticket.ticket_type == 'standard':
        total_price = ticket.quantity_booked * ticket.event.price_standard
    else:
        total_price = ticket.quantity_booked * ticket.event.price_premium
    
    return render(request, 'userpanel/ticket_detail.html', {'ticket': ticket, 'total_price': total_price})


@login_required(login_url='/404/')
def user_profile(request):
    # Fetch the profile for the logged-in user
    profile = Profile.objects.get(user=request.user)

    # Fetch the tickets booked by the logged-in user
    booked_tickets = Ticket.objects.filter(user=request.user)

    # Check if any ticket’s event date is within 20 days
    for ticket in booked_tickets:
        event_date = ticket.event.date
        days_until_event = (event_date - timezone.now().date()).days
        # Add a flag to each ticket to indicate if it is within 20 days
        ticket.non_cancelable = days_until_event <= 20

    # Pass the profile and booked tickets to the template
    context = {
        'profile': profile,
        'booked_tickets': booked_tickets,
    }
    
    return render(request, 'userpanel/user_profile.html', context)




@login_required(login_url='/404/')
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'userpanel/edit_profile.html', context)

@login_required(login_url='/404/')
def validate_expiry_date(expiry_date):
    try:
        expiry = datetime.strptime(expiry_date, "%m/%y")
        now = datetime.now().replace(day=1)  # Start of the current month
        return expiry >= now
    except ValueError:
        return False

@login_required(login_url='/404/')
# Function to validate the bank account
def validate_account(card_number, cvv, expiry_date):
    try:
        account = BankAccount.objects.get(card_number=card_number, cvv=cvv)
        if validate_expiry_date(expiry_date):
            return account
        else:
            return None
    except BankAccount.DoesNotExist:
        return None




@login_required(login_url='/404/')
def refund(request, ticket_id):
    
    # Retrieve ticket details
    ticket = get_object_or_404(Ticket, id=ticket_id)
    event = ticket.event
    ticket_type = ticket.ticket_type
    ticket_count = ticket.quantity_booked

    # Calculate refund amount
    ticket_price = event.price_premium if ticket_type == 'premium' else event.price_standard
    seat_count = ticket_count
    
    refund_amount = (ticket_price * seat_count) 

    form = AccountCheckForm(request.POST or None)
    account_number = None
    account_balance = None
    show_modal = False  # Flag to control modal display
    account = None

    # Reset session variable on initial page load (GET request)
    if request.method == "GET":
        request.session['account_verified'] = False

    if request.method == "POST":
        # Account validation process
        if 'validate_account' in request.POST and form.is_valid():
            card_number = form.cleaned_data["card_number"]
            cvv = form.cleaned_data["cvv"]
            expiry_date = form.cleaned_data["card_expiry_date"]

            account = validate_account(card_number, cvv, expiry_date)
            if account:
                # Store account details in session if verification is successful
                request.session['account_verified'] = True
                request.session['account_number'] = account.account_number
                request.session['account_balance'] = float(account.balance)
                account_number = account.account_number
                account_balance = account.balance
                messages.success(request, "Account verified successfully.")
                show_modal = True  # Set flag to display the modal
            else:
                request.session['account_verified'] = False
                messages.error(request, "No matching account found or the card has expired.")

        # Refund processing when refund button is clicked
        elif 'refund_now' in request.POST and request.session.get('account_verified'):
            account_number = request.session.get('account_number')
            account_balance = Decimal(request.session.get('account_balance'))

            try:
                account = BankAccount.objects.get(account_number=account_number)
            except BankAccount.DoesNotExist:
                messages.error(request, "Bank account not found.")
                return redirect('refund')  # Redirect back if account doesn't exist

            # Process refund and update seat availability
            if account:
                # Ensure account balance is updated with refund
                account.balance += refund_amount
                account.save()

                # Update event seat availability based on ticket type
                if ticket_type == 'premium':
                    event.seats_available_premium += seat_count
                    event.quantity_sold_premium -= seat_count
                else:
                    event.seats_available_standard += seat_count
                    event.quantity_sold_standard -= seat_count
                event.save()

                # Cancel the ticket
                ticket.status = 'canceled'
                ticket.save()

                # Clear session data after refund
                request.session.pop('account_verified', None)
                request.session.pop('account_number', None)
                request.session.pop('account_balance', None)

                messages.success(request, "Refund processed successfully.")
                return redirect("payment_success")  # Redirect to a success page after refund
            else:
                messages.error(request, "Refund could not be processed due to account issue.")

    # Retrieve account balance and account_number from session if verified
    account_verified = request.session.get('account_verified', False)
    if account_verified:
        account_number = request.session.get('account_number')
        account_balance = Decimal(request.session.get('account_balance'))
    if account:
        bank_name = account.bank_name
    else:
        bank_name = None  # If account is not available, set to None
    
    context = {
        'ticket': ticket,
        'form': form,
        'account_verified': account_verified,
        'account_balance': account_balance if account_verified else None,
        'refund_amount': refund_amount,
        'account_number': account_number,
        'bank_name': bank_name,
        'show_modal': show_modal,  # Pass show_modal to template
    }

    return render(request, 'userpanel/refund.html', context)



@login_required(login_url='/404/')
def user_reset_pass(request):
    # If the request is a POST 
    if request.method == 'POST':  
        # Create form with submitted data and current user
        form = ResetForm(user=request.user, data=request.POST) 
        # Check if the form data is valid 
        if form.is_valid(): 
            # Save the new password to the database 
            form.save()  
            # Show success message
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('site_login')  
        else:

            messages.error(request, 'Please correct the errors below.')  # Show error message
    else:
         # Create form for resetting the password if not a POST request
        form = ResetForm(user=request.user) 
    return render(request, 'userpanel/user_reset_pass.html',{'form':form})

@login_required(login_url='/404/')
def payment_page(request, event_id, ticket_type='standard', ticket_count=1):
    event = get_object_or_404(Event, id=event_id)
    ticket_price = event.price_premium if ticket_type == 'premium' else event.price_standard
    seat_count = int(ticket_count)
    service_charge = Decimal(10.00)
    total_amount = (ticket_price * seat_count) + service_charge

    form = AccountCheckForm(request.POST or None)
    account_balance = None
    account_number = None
    account=None

    # Reset session variable on initial page load (GET request)
    if request.method == "GET":
        request.session['account_verified'] = False

    if request.method == "POST":
        # Account validation process
        if 'validate_account' in request.POST and form.is_valid():
            
            card_number = form.cleaned_data["card_number"]
            cvv = form.cleaned_data["cvv"]
            expiry_date = form.cleaned_data["card_expiry_date"]

            account = validate_account(card_number, cvv, expiry_date)
            if account:
                request.session['account_verified'] = True
                request.session['account_number'] = account.account_number
                request.session['account_balance'] = str(account.balance)
                messages.success(request, "Account verified successfully.")
            else:
                request.session['account_verified'] = False
                messages.error(request, "No matching account found or the card has expired.")

        # Payment processing
        elif 'pay_now' in request.POST and request.session.get('account_verified'):
            account_number = request.session.get('account_number')
            account_balance = Decimal(request.session.get('account_balance'))
            
            account = BankAccount.objects.get(account_number=account_number)

            if account and account.balance >= total_amount:
                if (ticket_type == 'premium' and event.seats_available_premium >= seat_count) or \
                   (ticket_type == 'standard' and event.seats_available_standard >= seat_count):

                    account.balance -= total_amount
                    account.save()

                    if ticket_type == 'premium':
                        event.seats_available_premium -= seat_count
                        event.quantity_sold_premium += seat_count
                    else:
                        event.seats_available_standard -= seat_count
                        event.quantity_sold_standard += seat_count
                    event.save()

                    Ticket.objects.create(
                        event=event,
                        user=request.user,
                        ticket_type=ticket_type,
                        quantity_booked=seat_count,
                        status='booked'
                    )

                    request.session.pop('account_verified', None)
                    request.session.pop('account_number', None)
                    request.session.pop('account_balance', None)

                    messages.success(request, "Payment successful! Your ticket is booked.")
                    return redirect("payment_success")
                else:
                    messages.error(request, "Not enough seats available.")
            else:
                messages.error(request, "Insufficient balance or invalid account details.")

    account_balance = request.session.get('account_balance')
    account_number = request.session.get('account_number')
    if account:
        bank_name = account.bank_name
    else:
        bank_name = None  # If account is not available, set to None

    context = {
        'event': event,
        'ticket_type': ticket_type,
        'ticket_count': ticket_count,
        'total_amount': total_amount,
        'service_charge': service_charge,
        'form': form,
        'account_verified': request.session.get('account_verified', False),
        'account_balance': account_balance,
        'account_number': account_number,
        'user': request.user,
        'bank_name': bank_name,
        'seats_available_standard': event.seats_available_standard,
        'seats_available_premium': event.seats_available_premium,
        'quantity_sold_standard': event.quantity_sold_standard,
        'quantity_sold_premium': event.quantity_sold_premium,
    }

    return render(request, 'userpanel/payment_page.html', context)


@login_required(login_url='/404/')
def payment_success(request):
    try:
        # Try to retrieve the bank account associated with the current user
        bank_account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        bank_account = None  # Set to None if no bank account exists
    
    context = {
        'bank_account': bank_account,
    }

    return render(request, 'userpanel/payment_success.html', context)

@login_required(login_url='/404/')
def like_dislike_review(request, review_id, action):
    if request.method == "POST" and request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)

        # Fetch or create user's like/dislike record for the review
        obj, created = ReviewLikeDislike.objects.get_or_create(review=review, user=request.user)

        if action == "like":
            if obj.is_like is not True:  # Toggle like
                review.likes += 1  # Increment likes
                if obj.is_like is False:  # If previously disliked
                    review.dislikes -= 1  # Decrement dislikes
                obj.is_like = True
        elif action == "dislike":
            if obj.is_like is not False:  # Toggle dislike
                review.dislikes += 1  # Increment dislikes
                if obj.is_like is True:  # If previously liked
                    review.likes -= 1  # Decrement likes
                obj.is_like = False

        obj.save()
        review.save()

        return redirect('view_event', event_type=review.event.event_type, event_id=review.event.id)

    return redirect('404')


@login_required(login_url='/404/')
def add_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure review is only for movie events
    if event.event_type != 'movie':
        return render(request, 'userpanel/userhome.html', {'message': 'Reviews are only allowed for movie events.'})

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review = form.save(commit=False)  # Don't save yet, because we need to set user and event
            review.user = request.user
            review.event = event
            review.save()
            return redirect('view_event',event_type=event.event_type, event_id=event.id)
    else:
        form = ReviewForm()

    return render(request, 'userpanel/add_review.html', {'form': form, 'event': event})




@login_required(login_url='/404/')
def edit_review(request, event_id, review_id):
    event = get_object_or_404(Event, id=event_id)
    review = get_object_or_404(Review, id=review_id)

    # Ensure the logged-in user is the one who created the review
    if review.user != request.user:
        return render(request, 'userpanel/userhome.html', {'message': 'You are not authorized to edit this review.'})

    # Ensure the event is the same
    if review.event != event:
        return render(request, 'userpanel/userhome.html', {'message': 'This review does not belong to the event.'})

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()  # Save the updated review
            return redirect('view_event', event_type=event.event_type, event_id=event.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'userpanel/edit_review.html', {'form': form, 'event': event, 'review': review})


@login_required(login_url='/404/')
def register_interest(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event_type = event.event_type

    # Check if the user has already expressed interest
    if Interest.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "You have already registered your interest for this event.")
    else:
        # Register interest
        Interest.objects.create(event=event, user=request.user)
        messages.success(request, "Click on 'Interested' to stay updated about this event.")

    # Redirect back to the event page
    return redirect('view_event', event_type=event_type, event_id=event.id)

@login_required(login_url='/404/')
def delete_review(request, review_id):
    if request.method == "POST":
        # Fetch the review, ensuring it belongs to the logged-in user
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        messages.success(request, "Your review has been deleted successfully.")
    else:
        messages.error(request, "Invalid request.")
    return redirect('userhome')

@login_required(login_url='/404/')
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'userpanel/user_notifications.html', {'notifications': notifications})

@login_required(login_url='/404/')
def user_logout(request):
    # Log out the user.
    auth_logout(request)
   
    # Redirect to the home page after logging out.
    return redirect('sitehome')