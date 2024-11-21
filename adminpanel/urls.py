from django.urls import path

from adminpanel.views import admin_login, admin_notification, admin_org_profile, adminhome, hide_event, hide_review, show_event, movieslist, approve_events, event_deletion, approve_event_deletion, reject_event_deletion, userlist, logout, event_list, sports_list, plays_list, activities_list, organizer_list, admin_reset_pass, add_venue, view_each_event, view_venue, edit_venue, delete_venue, admin_user_profile

urlpatterns = [
    path('', admin_login, name = 'admin_login'), 
    
    path('adminhome/', adminhome, name = 'adminhome'), 
    path('movieslist/', movieslist, name='movieslist'),
    path('approve-events/', approve_events, name='approve_events'),
    path('event_deletion/', event_deletion, name='event_deletion'),
    path('approve_event_deletion/<int:request_id>/', approve_event_deletion, name='approve_event_deletion'),
    path('reject_event_deletion/<int:request_id>/', reject_event_deletion, name='reject_event_deletion'),
    path('admin_notification/', admin_notification, name='admin_notification'),
    path('userlist/', userlist, name='userlist'),
    path('logout/', logout, name='logout'),
    path('event_list/', event_list, name='event_list'),
    path('sports_list/', sports_list, name='sports_list'),
    path('plays_list/', plays_list, name='plays_list'),
    path('activities_list/', activities_list, name='activities_list'),
    path('organizer_list/', organizer_list, name='organizer_list'),
    path('admin_reset_pass/', admin_reset_pass, name='admin_reset_pass'),
    path('add_venue/', add_venue, name='add_venue'),
    path('view_venue/', view_venue, name='view_venue'),
    path('venue/edit/<int:id>/', edit_venue, name='edit_venue'),
    path('delete_venue/<int:venue_id>/', delete_venue, name='delete_venue'),
    path('admin_user_profile/<int:user_id>/', admin_user_profile, name='admin_user_profile'),
    path('view_each_event/<int:event_id>/', view_each_event, name = 'view_each_event'),
    path('admin_org_profile/<int:organizer_id>/', admin_org_profile, name='admin_org_profile'),
    path('hide_event/<str:event_type>/<int:event_id>/', hide_event, name='hide_event'),
    path('show_event/<str:event_type>/<int:event_id>/', show_event, name='show_event'),
    path('hide_review/<int:review_id>/', hide_review, name='hide_review'),
    path('logout/', logout, name='logout'),
]