# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings

# def send_registration_email(email, username):
#     context = {'username': username}
#     email_subject = 'Welcome to Our Platform'
#     email_body = render_to_string('sitevisitor/reg_success.txt', context)

#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )

#     return my_email.send(fail_silently=False)


# def send_otp_email(email, otp_code):
#     context = {
#         'otp_code': otp_code,
#     }

#     email_subject = 'Your OTP for Password Reset'
#     email_body = render_to_string('sitevisitor/otp_email.txt', context)

#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )
#     return my_email.send(fail_silently=False)


# # Function to send the confirmation email after OTP verification
# def send_verification_email(email):
#     context = {}  # Add any necessary context if needed

#     email_subject = 'OTP Verified Successfully'
#     email_body = render_to_string('sitevisitor/otp_verified.txt', context)

#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )
#     return my_email.send(fail_silently=False)
