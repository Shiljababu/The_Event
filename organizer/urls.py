from django.urls import path
from .views import drafts, org_login, org_register, org_home, attendees, org_profile, add_event, edit_event, delete_event, contact_form, hidden_events, notification, edit_org_profile, org_reset_pass, org_view_event, org_forgot, org_otp, logout
urlpatterns = [
    path('', org_register, name = 'org_register'),
    path('org_login/', org_login, name = 'org_login'),  
    path('org_home/', org_home, name = 'org_home'), 
    path('attendees/', attendees, name = 'attendees'),   
    path('org_profile/', org_profile, name = 'org_profile'), 
    path('add_event/', add_event, name = 'add_event'), 
    path('edit_event/<int:event_id>/', edit_event, name = 'edit_event'), 
    path('delete-event/<int:event_id>/', delete_event, name='delete_event'),
    path('notification/', notification, name='notification'),
    path('contact_form/<int:event_id>/', contact_form, name = 'contact_form'), 
    path('hidden_events/', hidden_events, name='hidden_events'),
    path('edit_org_profile/', edit_org_profile, name='edit_org_profile'),
    path('org_reset_pass/', org_reset_pass, name='org_reset_pass'),
    path('org_view_event/<str:event_type>/<int:event_id>/', org_view_event, name='org_view_event'),
    path('drafts/', drafts, name='drafts'),
    path('org_forgot/', org_forgot, name = 'org_forgot'),
    path('org_otp/', org_otp, name = 'org_otp'),
    path('logout/', logout, name='logout'),
]