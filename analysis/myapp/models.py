# from djongo import models

# class Users(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=10)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djongo import models

class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        # Create and save a new user
        user = self.model(nclearame=name, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=8)

    #adding users
    objects = UserManager()

    # Specify the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','password']

    # def __str__(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True
