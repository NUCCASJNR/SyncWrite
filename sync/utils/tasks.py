#!/usr/bin/env python3

"""Celery task handler"""

from sync.utils.email_utils import EmailUtils
from celery import shared_task
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@shared_task
def send_verification_email_async(user, verification_code):
    EmailUtils.send_verification_email(user, verification_code)

@shared_task
def send_new_login_detected_email_async(user, ip_address):
    logger.info(f"New login detected for user {user.username}")
    EmailUtils.send_new_login_detected_email(user, ip_address)
    
def send_reset_password_email_async(user, reset_code):
    EmailUtils.send_reset_password_email(user, reset_code)