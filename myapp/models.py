from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        # Create and save a new user
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
