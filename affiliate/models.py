from django.db import models
from django.urls import reverse

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.conf import settings

User = settings.AUTH_USER_MODEL









class Buss_Schedule(models.Model):
    bus_pic = models.ImageField(null=True, blank=True, upload_to='images/buses')
    dest_pic=models.ImageField(null=True, blank=True, upload_to='images/destinations')
    destination=models.CharField(max_length=255, null=True, blank=True)
    departure=models.CharField(max_length=255, null=True, blank=True)
    trip_duration=models.CharField(max_length=255, null=True, blank=True)
    trip_distance=models.CharField(max_length=255, null=True, blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.destination} | {self.departure}"
    def get_absolute_url(self):
        # return reverse("article_details",args=(str(self.id)))
        return reverse("home")

class Sit(models.Model):
    number=models.CharField(max_length=255)
    booking=models.ManyToManyField(User)
    schedule=models.ForeignKey(Buss_Schedule,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.number}"

class Book(models.Model):
    user=models.ManyToManyField(User)
    sits=models.ManyToManyField(Sit)
    trip=models.ForeignKey(Buss_Schedule,on_delete=models.CASCADE)




class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)


        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username,  password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):


    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    ADULT = 'AD'
    STUDENT = 'SD'
    SCHOOLER = 'SC'

    STATUS_CHOIES = [
        (ADULT, 'Adult'),
        (STUDENT, 'Student'),
        (SCHOOLER, 'Schooler'),

    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOIES,
        default=ADULT,
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password','status']

    def __str__(self):
        return self.username




