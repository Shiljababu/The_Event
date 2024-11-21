# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings

# def send_registration_email(email, username):
#     """
#     Sends a registration email to the organizer.
#     """
#     context = {'username': username}
#     email_subject = 'Welcome to the Organizer Platform'
#     email_body = render_to_string('organizer/org_reg_success.txt', context)

#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )

#     return my_email.send(fail_silently=False)


# def send_otp_email(email, otp_code):
#     """
#     Sends an OTP email to the organizer.
#     """
#     context = {'otp_code': otp_code}
#     email_subject = 'Your OTP for Password Reset'
#     email_body = render_to_string('organizer/org_otp_email.txt', context)

#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )
#     return my_email.send(fail_silently=False)


# def send_verification_email(email):
#     """
#     Sends a confirmation email after OTP verification.
#     """
#     context = {}  # Add any necessary context if needed

#     email_subject = 'OTP Verified Successfully'
#     email_body = render_to_string('organizer/org_otp_verified.txt', context)

#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )
#     return my_email.send(fail_silently=False)
