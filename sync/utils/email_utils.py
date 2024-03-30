#!/usr/bin/env python3

"""
Handles all utils relating to sending emails and also generating tokens
"""
from django.conf import settings
from os import getenv
from sync.utils.redis_utils import RedisClient
from sync.models.user import MainUser as User
import secrets
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv("ELASTIC_EMAIL_KEY")
SENDER = getenv("EMAIL_SENDER")


class EmailUtils:
    @staticmethod
    def generate_verification_code(length=6):
        """
        Generate a random verification code.
        :param length: Length of the verification code (default is 6)
        :return: Random verification code
        """
        charset = "0123456789"
        verification_code = ''.join(secrets.choice(charset) for _ in range(length))
        return verification_code

    @staticmethod
    def generate_verification_link(user_id, verification_code):
        """
        Generates the verification link based on the user_id and verification_code
        """
        return f"{settings.BASE_URL}/verify/{user_id}/{verification_code}/"

    @staticmethod
    def send_verification_email(user, verification_code):
        url = "https://api.elasticemail.com/v2/email/send"
        # context = {
        #     'verification_code': verification_code,
        #     'first_name': user.first_name,
        #     'last_name': user.last_name,
        # }
        # html_template = render_to_string("parent/second.html", context)
        redis_client = RedisClient()
        key = f'user_id:{user.id}:{verification_code}'
        request_payload = {
            "apikey": API_KEY,
            "from": getenv("EMAIL_SENDER"),
            "to": user.email,
            "subject": "Verify your account",
            "bodyHtml": f"Hello {user.username}, <p>Welcome to REntEase,"
                        f" Getting apartment couldn't have been much easier"
                        f"<p> <br> Your verification code is: {verification_code}</br>",
            "isTransactional": False,
        }

        try:
            response = requests.post(url, data=request_payload)
            if response.status_code == 200:
                if response.json()['success']:
                    redis_client.set_key(key, verification_code, expiry=30)
                    return True
            else:
                print(f'Error sending verification email to {user.email}')
                return False
        except Exception as e:
            print(f'Error sending verification email to {user.email}: {str(e)}')
            return False

    @staticmethod
    def send_password_reset_email(user: User, reset_code: int):
        """
        Sends a password-reset email to the user
        """
        redis_client = RedisClient()
        key = f'reset_token:{user.id}:{reset_code}'
        redis_client.set_key(key, reset_code, expiry=30)
        url = "https://api.elasticemail.com/v2/email/send"
        request_payload = {
            "apikey": API_KEY,
            "from": getenv("EMAIL_SENDER"),
            "to": user.email,
            "subject": "Reset your password",
            "bodyHtml": f"Hello {user.first_name} {user.last_name},<br> Your password reset code is: {reset_code}</br>",
            "isTransactional": False
        }
        try:
            response = requests.post(url, data=request_payload)
            if response.status_code == 200:
                return True
            else:
                print(f'Error sending password reset email to {user.email}')
                return False
            
        except Exception as e:
            print(f'Error sending password reset email to {user.email}: {e}')
            return False

