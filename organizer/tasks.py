# from celery import shared_task
# from celery.utils.log import get_task_logger
# from .email import send_registration_email, send_otp_email, send_verification_email

# # Logger for tasks
# logger = get_task_logger(__name__)

# @shared_task(name="organizer_send_registration_email_task", bind=True)
# def send_registration_email_task(self, email, username):
#     """
#     Task to send a registration email to the organizer.
#     """
#     logger.info(f"Sending registration email to organizer: {email}")
#     return send_registration_email(email=email, username=username)


# @shared_task(name="organizer_send_otp_email_task")
# def send_otp_email_task(email, otp_code):
#     """
#     Task to send OTP email to the organizer.
#     """
#     logger.info(f"Sending OTP email to organizer: {email}")
#     return send_otp_email(email, otp_code)


# @shared_task(name="organizer_send_verification_email_task")
# def send_verification_email_task(email):
#     """
#     Task to send a verification email to the organizer.
#     """
#     logger.info(f"Sending verification email to organizer: {email}")
#     return send_verification_email(email)
