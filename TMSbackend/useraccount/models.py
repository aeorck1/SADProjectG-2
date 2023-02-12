from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
    BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """Create and save a new User model instance"""

        if not email:
            raise ValueError("Email cannot be None or empty")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)

        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Create and save new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """A custom user model"""

    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'