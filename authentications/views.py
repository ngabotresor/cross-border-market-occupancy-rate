# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
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

        if user.is_approved == True or user.is_approved == False:
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
    

#View to list users with viewer role 

class ViewerList(APIView):
    permission_classes = [IsAuthenticated, IsHeaderUser]
    def get(self, request, format=None):
        users = User.objects.filter(role__name='viewer')
        serializer = UserSerializer(users, many=True)
        return Response({
            "message": "Viewers retrieved successfully",
            "users": serializer.data
        }, status=status.HTTP_200_OK)


# View to approve a user
class UpdateUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk, format=None):
        serializer = UserUpdateSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=pk)
            if 'is_approved' in serializer.validated_data:
                user.is_approved = serializer.validated_data['is_approved']
            if 'role' in serializer.validated_data:
                role_name = serializer.validated_data['role']
                role = Role.objects.get(name=role_name)
                user.role = role
            user.save()
            return Response({
                "message": "User updated successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "Failed to update user",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
