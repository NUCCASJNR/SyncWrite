#!/usr/bin/env python3
"""contains all the authentication related views"""
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from sync.models.user import MainUser, hash_password
from sync.serializers.auth import (
    SignUpSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer
)
from sync.utils.tasks import (
    send_verification_email_async,
    EmailUtils,
    send_new_login_detected_email_async,
    send_reset_password_email_async
)
from sync.utils.redis_utils import RedisClient
from sync.utils.auth import get_client_ip
from sync.models.address import IPAddress
from uuid import uuid4
from django.core.exceptions import ObjectDoesNotExist


class SignUpViewSet(viewsets.ModelViewSet):
    """Signup View"""

    serializer_class = SignUpSerializer
    queryset = MainUser.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a new user"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            verification_code = EmailUtils.generate_verification_code()
            hashed_password = hash_password(
                serializer.validated_data["password"])
            serializer.validated_data["password"] = hashed_password
            user = MainUser.custom_save(**serializer.validated_data,
                                        verification_code=verification_code)
            send_verification_email_async(user, verification_code)
            client_ip=get_client_ip(request)
            IPAddress.custom_save(address=client_ip, user=user)
            return Response({
                "message":
                    "You have successfully signed up. Please check your"
                    " email for the verification code",
                "status":
                    status.HTTP_201_CREATED,
            })
        else:
            errors = serializer.errors
            if "username" and "email" in errors:
                errors = {
                    "error": "User with this email and username already exists",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            if "email" in errors and errors["email"][0] == "main user with this email already exists.":
                errors = {
                    "error": "User with this email already exists",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            if "username" in errors and errors["username"][0] == "main user with this username already exists.":
                errors = {
                    "error": "User with this username already exists",
                    "status": status.HTTP_400_BAD_REQUEST
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerficationView(APIView):
    """View for verifying user's email address"""

    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        """Create a new user

        :param request: The request object
        :param args: The args
        :param kwargs: The keyword args
        :returns: The response

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data["verification_code"]
            user = MainUser.custom_get(**{"verification_code": code})
            key = None
            if user is not None:
                key = f"user_id:{user.id}:{code}"
                if user.is_verified:
                    return Response({
                        "message": "Your account has already been verified",
                        "status": 200,
                    })
            redis_cli = RedisClient()
            if user and redis_cli.get_key(key):
                print(redis_cli.get_key(key))
                MainUser.custom_update(
                    filter_kwargs={"verification_code": code},
                    update_kwargs={"is_verified": True},
                )
                redis_cli.delete_key(key)
                return Response({
                    "message":
                    "Your Account has been successfully verified, You can now login!",
                    "status": status.HTTP_200_OK,
                })                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            return Response({ 
                "error": "Invalid or expired verification code",
                "status": status.HTTP_400_BAD_REQUEST,
            })
        return Response({
            "error": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


class LoginView(APIView):
    """View for logging in a user"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """Log in a user

        :param request: The request object
        :param args: The args
        :param kwargs: The keyword args
        :returns: The response

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if not user.is_verified:
                    return Response({
                        "error": "You need to verify your account to login",
                        "status": status.HTTP_400_BAD_REQUEST,
                    })

                ip = get_client_ip(request)
                ip_addresses = IPAddress.objects.filter(address=ip, user=user)
                if ip_addresses.exists():
                    # If there are IP addresses associated with the user and current IP matches
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "You have successfully logged in",
                        "access_token": str(refresh.access_token),
                        "status": status.HTTP_200_OK,
                    })
                elif IPAddress.objects.filter(user=user).exists():
                    # If there are IP addresses associated with the user but current IP doesn't match
                    device_id = str(uuid4())
                    request.session['device_id'] = f'{user.id}:{device_id}'
                    send_new_login_detected_email_async(user, ip)
                    return Response({
                        'message': 'We noticed a suspicious login attempt, please verify your device to continue',
                        'status': status.HTTP_400_BAD_REQUEST
                    })
                else:
                    # If no IP addresses associated with the user
                    return Response({
                        "error": "No IP addresses associated with the user",
                        "status": status.HTTP_400_BAD_REQUEST,
                    })

            return Response({
                "error": "Invalid email or password",
                "status": status.HTTP_400_BAD_REQUEST,
            })
        return Response({
            "error": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


class LoginView(APIView):
    """View for logging in a user"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """Log in a user

        :param request: The request object
        :param args: The args
        :param kwargs: The keyword args
        :returns: The response

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if not user.is_verified:
                    return Response({
                        "error": "You need to verify your account to login",
                        "status": status.HTTP_400_BAD_REQUEST,
                    })

                ip = get_client_ip(request)
                ip_addresses = IPAddress.objects.filter(address=ip, user=user)
                if ip_addresses.exists():
                    # If there are IP addresses associated with the user and current IP matches
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "You have successfully logged in",
                        "access_token": str(refresh.access_token),
                        "status": status.HTTP_200_OK,
                    })
                elif IPAddress.objects.filter(user=user).exists():
                    # If there are IP addresses associated with the user but current IP doesn't match
                    device_id = str(uuid4())
                    request.session['device_id'] = f'{user.id}:{device_id}'
                    send_new_login_detected_email_async(user, ip)
                    return Response({
                        'message': 'We noticed a suspicious login attempt, please verify your device to continue',
                        'status': status.HTTP_400_BAD_REQUEST
                    })
                else:
                    # If no IP addresses associated with the user
                    return Response({
                        "error": "No IP addresses associated with the user",
                        "status": status.HTTP_400_BAD_REQUEST,
                    })

            return Response({
                "error": "Invalid email or password",
                "status": status.HTTP_400_BAD_REQUEST,
            })
        return Response({
            "error": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        })


class VerifyDeviceView(APIView):
    """View for verifying a device"""

    def post(self, request, *args, **kwargs):
        """Verify a device

        :param request: The request object
        :param args: The args
        :param kwargs: The keyword args
        :returns: The response

        """
        ip = get_client_ip(request)
        code = request.data
        redis_client = RedisClient()
        user_id = request.session['device_id'].split(':')[0]
        user = MainUser.custom_get(**{'id': user_id})
        key = f'Device:{ip}:{code}'
        if redis_client.get_key(key):
            IPAddress.custom_save(address=ip, user=user)
            redis_client.delete_key(key)
            return Response({
                'message': 'Device has been successfully verified',
                'status': status.HTTP_200_OK
            })
        return Response({
            'error': 'Invalid or expired verification code',
            'status': status.HTTP_400_BAD_REQUEST
        })
    

class ResetPasswordView(APIView):
    """
    View for resetting user password
    """
    serializer_class = ResetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = MainUser.custom_get(**{'email': email})
            reset_code = EmailUtils.generate_verification_code()
            if user is not None:
                send_reset_password_email_async(user, reset_code)
                MainUser.custom_update(
                    filter_kwargs={'email': email},
                    update_kwargs={'reset_code': reset_code}
                )
                return Response({
                    'message': 'Kindly check your mail for the verification code',
                    'status': status.HTTP_200_OK
                })
            return Response({
                'error': 'Invalid email, kindly check the email provided and try again',
                'status': status.HTTP_400_BAD_REQUEST
            })
        else:
            return Response({
                'error': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST
            })


class CreateNewPasswordView(APIView):
    """
    View for creating a new password
    """
    serializer_class = ChangePasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            reset_code = serializer.validated_data['reset_code']
            password = serializer.validated_data['password']
            redis_client = RedisClient()
            user = MainUser.custom_get(**{'reset_code': reset_code})
            if user is not None:
                user_id = user.id
                key = f'user:{user_id}:reset_code:{reset_code}'
                if redis_client.get_key(key):
                    MainUser.custom_update(
                        filter_kwargs={'reset_code': reset_code},
                        update_kwargs={'password': password, 'reset_code': None}
                    )
                    redis_client.delete_key(key)
                    return Response({
                        'message': 'Password has been successfully updated',
                        'status': status.HTTP_200_OK
                    })
                return Response({
                    'error': 'Invalid or expired verification code',
                    'status': status.HTTP_400_BAD_REQUEST
                })
            return Response({
                    'error': 'Invalid or expired verification code',
                    'status': status.HTTP_400_BAD_REQUEST
                })
        else:
            return Response({
                'error': serializer.errors,
                'status': status.HTTP_400_BAD_REQUEST
            })
            
            