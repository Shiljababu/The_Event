from django.urls import path
from .views import register, sitehome, site_login, site_otp, forgot, reset, error_page, org_reset


urlpatterns = [
    path('', sitehome, name = 'sitehome'), 
    path('register/', register, name = 'register'),
    path('site_login/', site_login, name = 'site_login'),
    path('site_otp/', site_otp, name = 'site_otp'),
    path('forgot_password/', forgot, name = 'forgot'),
    path('reset/', reset, name = 'reset'),
    path('org_reset/', org_reset, name = 'org_reset'),
    path('404/', error_page)
    
]