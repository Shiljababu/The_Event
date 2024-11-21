from django.urls import path


from .views import edit_review, like_dislike_review, register_interest, ticket_detail, user_logout, user_notifications, userhome, movies, events, user_profile, user_reset_pass, activities, sports, plays, ticket, view_event, payment_page, refund, payment_success, edit_profile, add_review, delete_review

urlpatterns = [
    path('', userhome, name = 'userhome'), 
    path('movies/', movies, name = 'movies'),
    path('events/', events, name = 'events'),
    path('sports/', sports, name = 'sports'),
    path('plays/', plays, name = 'plays'),
    path('activities/', activities, name = 'activities'), 
    path('view_event/<str:event_type>/<int:event_id>/', view_event, name='view_event'),
    path('user_profile/', user_profile, name = 'user_profile'),
    path('user_reset_pass/', user_reset_pass, name = 'user_reset_pass'),
    path('ticket/', ticket, name = 'ticket'),
    path('payment_page/<int:event_id>/<str:ticket_type>/<int:ticket_count>/', payment_page, name='payment_page'),
    path('refund/<int:ticket_id>/', refund, name = 'refund'),
    path('payment_success/', payment_success, name = 'payment_success'),
    path('edit_profile/', edit_profile, name = 'edit_profile'),
    path('add_review/<int:event_id>/', add_review, name = 'add_review'),
    path('review/<int:review_id>/<str:action>/', like_dislike_review, name='like_dislike_review'),
    path('register_interest/<int:event_id>/', register_interest, name='register_interest'),
    path('user_notifications', user_notifications, name='user_notifications'),
    path('edit_review/<int:event_id>/<int:review_id>', edit_review, name='edit_review'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('logout/', user_logout, name='user_logout'),
    
]