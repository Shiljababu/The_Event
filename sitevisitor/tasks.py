# # Create a task for sending registration email with a specific name
# from celery import shared_task
# from .email import send_otp_email, send_registration_email, send_verification_email
# from celery.utils.log import get_task_logger

# # Create a logger object to log messages for the current task
# logger = get_task_logger(__name__)

# @shared_task(name="send_registration_email_task", bind=True)
# def send_registration_email_task(self, email, username):

#     # Log a message that says we are sending a registration email
#     logger.info(f"Sending registration email to {email}")
    
#     # Call the function to send the registration email and return its result
#     return send_registration_email(email=email, username=username)

# # Create a task for sending OTP email with a specific name
# @shared_task(name="send_otp_email_task")
# def send_otp_email_task(email, otp_code):

#     # Log a message that says we are sending an OTP email
#     logger.info("Sending OTP email")

#     # Call the function to send the OTP email and return its result
#     return send_otp_email(email, otp_code)

# # Create a task for sending verification email with a specific name
# @shared_task(name="send_verification_email_task")
# def send_verification_email_task(email):

#     # Log a message that says we are sending a verification email
#     logger.info(f"Sending verification email to {email}")

#     # Call the function to send the verification email and return its result
#     return send_verification_email(email)
