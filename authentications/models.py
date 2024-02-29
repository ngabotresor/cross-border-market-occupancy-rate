from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


class Role(models.Model):
    creator = 'creator'
    viewer = 'viewer' # those in copy when sending a report to minister
    verifier = 'verifier' #supervisor, that person who verifies the report after being created
    approver = 'approver' # the person who approves the report after being verified
    header = 'header' #  the person who approves the report and send it to the minister
    minister = 'minister'
    admin = 'admin'

    ROLE_CHOICES = [
        (creator, 'creator'),
        (viewer, 'viewer'),
        (verifier, 'verifier'),
        (approver, 'approver'),
        (header, 'header'),
        (minister, 'minister'),
        (admin, 'admin'),
    ]

    name = models.CharField(max_length=10, choices=ROLE_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_role'
        ordering = ['id']

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True,blank=True, default=1)
    position = models.CharField(max_length=255)
    location = models.ForeignKey('marketrecord.Location', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    class Meta:
        db_table = 'user'

    

