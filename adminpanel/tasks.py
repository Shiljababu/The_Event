# from celery import shared_task
# from celery.utils.log import get_task_logger
# from .email import send_deactivation_email, send_activation_email


# # Create a logger object to log messages for the current task
# logger = get_task_logger(__name__)


# # Task to send the deactivation email
# @shared_task(name="send_deactivation_email_task", bind=True)
# def send_deactivation_email_task(self, email, username, role=None):


#     # Log a message that says we are sending an account deactivation email
#     logger.info(f"Sending account deactivation email to {email}")


#     # Call the function to send the deactivation email and return its result
#     return send_deactivation_email(email=email, username=username)


# # Task to send the activation email
# @shared_task(name="send_activation_email_task", bind=True)
# def send_activation_email_task(self, email, username, role=None):


#     # Log a message that says we are sending an account activation email
#     logger.info(f"Sending account activation email to {email}")
    
#     # Call the function to send the activation email and return its result
#     return send_activation_email(email=email, username=username)

