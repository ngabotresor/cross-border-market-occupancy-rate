# urls.py
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('create-user/', UserCreate.as_view(), name='create-user'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all-users/', UserList.as_view(), name='all-users'),
    path('update-user/<int:pk>/', UpdateUser.as_view(), name='update-user'),
]