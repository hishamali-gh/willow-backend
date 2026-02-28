from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        name = extra_fields.get('name')

        if not name or not name.strip():
            raise ValidationError('*Name is required')

        if not username or not username.strip():
            raise ValidationError('*Username is required')

        if not email or not email.strip():
            raise ValidationError('*Email is required')
        
        extra_fields['name'] = name.strip()
        username = username.strip()
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password)

        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValidationError('*Superuser must have a password')

        if extra_fields.get('is_staff') is not True:
            raise ValidationError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValidationError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.username
