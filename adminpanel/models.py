from django.db import models
from django.contrib.auth.models import User, Group


class Profile(models.Model):
    ROLE_CHOICES = (
        ('organizer', 'Organizer'),
        ('user', 'User')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    profile_description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    id_proof = models.ImageField(upload_to='id_proof/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Venue(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    venue_image = models.ImageField(upload_to='venue_images/')  

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('event', 'Event'),
        ('play', 'Play'),
        ('activity', 'Activity'),
        ('sport', 'Sport'),
    ]

    STATUS_CHOICES = [
        ('visible', 'Visible'),
        ('hidden', 'Hidden'),
        ('draft', 'Draft')
    ]

    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'organizer'})
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='event')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    event_image = models.ImageField(upload_to='event_image/', blank = True, null=True)
    location = models.CharField(max_length=255)
    is_cancelled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='hidden')
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True) 
    
    price_standard = models.DecimalField(max_digits=10, decimal_places=2)
    price_premium = models.DecimalField(max_digits=10, decimal_places=2)
    seats_available_standard = models.PositiveIntegerField(default=0)  
    seats_available_premium = models.PositiveIntegerField(default=0)   
    quantity_sold_standard = models.PositiveIntegerField(default=0)
    quantity_sold_premium = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

# Ticket model for managing event tickets
def get_admin_user_id():
    # Change 'admin' to the appropriate username if needed
    return User.objects.get(username='admin').id


# Ticket model for managing event tickets
class Ticket(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('canceled', 'Canceled'),
        
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_admin_user_id)
    ticket_type = models.CharField(max_length=10, choices=(('standard', 'Standard'), ('premium', 'Premium')), default='standard')
    quantity_booked = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ticket_type.capitalize()} Ticket(s) for {self.event.title}"


class EventDeletionRequest(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    reason = models.TextField()  
    requested_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Deletion request for {self.event.title} by {self.organizer.username}"




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"



    
class BankAccount(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('closed', 'Closed'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True, default="account_0001") 
    card_number = models.CharField(max_length=10, unique=True)
    card_expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    currency = models.CharField(max_length=3, default='USD')
    bank_name = models.CharField(max_length=100, default='Default Bank')  
    
    def __str__(self):
        return f"{self.user.username}'s Bank Account"


class Review(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=(('visible', 'Visible'), ('hidden', 'Hidden')), default='visible')
    likes = models.PositiveIntegerField(default=0)  # Count of likes
    dislikes = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Review for {self.event.title} by {self.user.username}"


class ReviewLikeDislike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(null=True)  # True for like, False for dislike, null for no action

    def __str__(self):
        action = "Liked" if self.is_like else "Disliked" if self.is_like is False else "No Action"
        return f"{self.user.username} {action} {self.review}"


class Interest(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('event', 'user')
        
    def __str__(self):
        return f"{self.user.username} interested in {self.event.title}"
