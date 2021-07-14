from __future__ import absolute_import, unicode_literals

from celery import task
from celery.utils.log import get_task_logger

from django.core.mail import BadHeaderError

from authapp.utils import Helper
from social_application.settings import EMAIL_HOST_USER


logger = get_task_logger(__name__)


@task(bind=True)
def send_email_task(self, data):
    """
    Send Email using Celery
    :param self:
    :param data: dict that contains email_subject, email_body, email
    """
    logger.info(f"from={EMAIL_HOST_USER}")
    try:
        logger.info("About to send_mail")
        Helper.send_account_verification_email(data)
        logger.info("Email Sent Successfully")
    except BadHeaderError:
        logger.info("BadHeaderError")
    except Exception as e:
        logger.error(e)