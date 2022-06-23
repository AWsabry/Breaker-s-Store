from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,Group





class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        """
        To make email login case sensetive.
        """
        
        return self.get(email__iexact=username)

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        
        if not email:
            raise ValueError('Email does not included!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        return self.create_user(email=email, password=password, **extra_fields)

class Profile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    Age = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=60, null=True)
    PhoneNumber =  models.CharField(max_length=20, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    ProfilePic = models.ImageField(upload_to="profile/", null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    email = models.EmailField(max_length=500, blank=True)
    def __str__(self):
        return self.email


        
    