# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings

# # Function to send the deactivation email
# def send_deactivation_email(email, username, role="user"):
#     context = {'username': username, 'role': role}
#     email_subject = f'Account Deactivation Notice ({role.capitalize()})'
#     email_body = render_to_string('adminpanel/deactivation_email.txt', context)
#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )
#     return my_email.send(fail_silently=False)

# # Function to send the activation email
# def send_activation_email(email, username, role="user"):
#     context = {'username': username, 'role': role}
#     email_subject = f'Account Activation Notice ({role.capitalize()})'
#     email_body = render_to_string('adminpanel/activation_email.txt', context)
#     my_email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email],
#     )
#     return my_email.send(fail_silently=False)
