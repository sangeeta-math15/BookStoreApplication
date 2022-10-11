from django.contrib import auth
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from .util import EncodeDecode
from rest_framework.response import Response
import logging
from django.conf import settings


class UserRegistration(APIView):
    """
       This api is for registration of new user
    """

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user_name = serializer.data.get('username')
            user_id = serializer.data.get('id')
            token = EncodeDecode.encode_token({"user_id": user_id, "username": user_name})
            send_mail(from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[serializer.data['email']],
                      message='Register yourself by complete this verification'
                              f'url is http://127.0.0.1:8000/user/verify_token/{token}',
                      subject='Link for the registration', )
            return Response({"message": "CHECK EMAIL for verification"})

        except ValueError as e:
            logging.exception(e)
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            logging.exception(e)
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.exception(e)
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    This class used to login the user
    """
    def post(self, request):
        try:
            user = auth.authenticate(username=request.data.get('username'), password=request.data.get('password'))
            if user:
                token = EncodeDecode.encode_token(payload={'user_id': user.id})
                return Response(
                    {
                        "message": "logged in successfully",
                        "data": {"token": token}
                    }, status=status.HTTP_202_ACCEPTED)

            # Login failed
            return Response({"message": "Login failed!"},
                            status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            logging.error(e)
            return Response({"Exception: Authentication failed.."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logging.error(e)
            return Response({'Exception': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(APIView):
    def get(self, request, token=None):
        try:
            d_token = EncodeDecode.decode_token(token)
            u_ = User.objects.filter(id=d_token.get("user_id"), username=d_token.get("username"))
            if u_ is not None:
                u_.is_verified = True
                return Response({"message": "Email Verified and Registered successfully"})
            return Response({"message": "Try Again......Wrong credentials"})
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)})
