# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import *
#user create view
class UserCreate(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'User creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

#login view

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid or missing fields', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_approved == True:
             refresh = RefreshToken.for_user(user)
             res = {
                    'message': 'User logged in successfully',
                    'user': UserSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
             return Response(res, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not approved'}, status=status.HTTP_400_BAD_REQUEST)

    

#user list view

class UserList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "message": "Users retrieved successfully",
            "users": serializer.data
        }, status=status.HTTP_200_OK)
    

# View to approve a user

class UserApprove(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request, pk, format=None):
        serializer = UserApproveSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=pk)
            user.is_approved = True
            user.save()
            return Response({
                "message": "User approved successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to approve user",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
