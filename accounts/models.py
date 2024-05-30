from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, is_active=True, is_staff=False, is_superuser=False):  # , **extra_fields
        if not email:
            raise ValueError('Users must have email address')

        if not username:
            raise ValueError('Users must have username')

        if not password:
            raise ValueError('Users must have password')

        # Normalize example: Test@gmail.com ---> test@gmail.com
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          date_joined=timezone.now())  # , **extra_fields
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.set_password(password)
        user.save()

        return user

    # Called when we run python manage.py createsuperuser
    def create_superuser(self, username, email, password=None):
        user = self.create_user(email, username, password,
                                is_staff=True, is_superuser=True)
        return user


# Abstract Base User will give three fields by default (id, password, last_login)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    # USERNAME_FIELD and password are required to login
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELD is a list of the field names that will be prompted
    # for when creating a user via the createsuperuser management command
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/', default='profile_pic/user.png')
    country = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True)

    def __str__(self):
        return self.user.email
