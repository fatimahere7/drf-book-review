from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer,UserRegistrationSerializer,UserProfileSerializer
from django.contrib.auth import logout

class UserRegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user= serializer.save()
            token, created=Token.objects.get_or_create(user=user)
            return Response({
                'token':token.key,
                'user':UserProfileSerializer(user).data
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
     permission_classes=[AllowAny]

     def post(self,request):
         serializer=UserLoginSerializer(data=request.data)
         if serializer.is_valid():
             user= serializer.validated_data['user']
             token,created=Token.objects.get_or_create(user=user)
             return Response({
                 'token':token.key,
                 'user':UserProfileSerializer(user).data
             },status=status.HTTP_200_OK)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)    


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)     