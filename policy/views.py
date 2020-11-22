import json

import jwt
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model as user_model
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated  
from rest_framework import viewsets
from rest_framework.views import  APIView
from .models import User,UserProfile
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status, views
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (EmailVerificationSerializer, LoginSerializer,
                          RegisterSerializer, RequestPasswordResetSerializer,
                          SetNEwPasswordSerializer, UserSerializer,UserProfileSerializer)
from .utils import Util


class RegisterAPI(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            u_id64=urlsafe_base64_encode(str(user.id).encode('utf-8'))
            u_id64 = u_id64
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('policy:password_reset',kwargs={'u_id64':u_id64,'token':token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hello  Use link below to reset password \n'+absurl
            data = {'email_body':email_body,'to_email':user.email,'email_subject':'Password Reset'}
            Util.send_email(data)
        return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(email=email, username=username, password=password)
    
        if user:
            auth_token = jwt.encode({"email": email}, 'rrffgguyuioommbf456788')

            serializer = LoginSerializer(user)

            user_data = User.objects.get(email=email)

            data = {
                'user': serializer.data, 'first_name': user_data.first_name, 'last_name':user_data.last_name, 'token': auth_token
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
    
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING, required=True)
    # token = openapi.Parameter('token', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email':'Successfully activated'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as identifier:

            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class SetNEwPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNEwPasswordSerializer

    def patch(self,requeest):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Success':True, 'messsage':'Password reset success'},status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):

    """
    Provides a get post put delete method handler.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):

        userprofiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(userprofiles, many=True)
        return Response(serializer.data)
    
    # def post(self,request):
      
    #     serializer = UserProfileSerializer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SingleUserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(pk)
        return Response(serializer.data)

    def put(self,request,pk):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

