# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import UserManager
from django.db import models

# class User(AbstractUser):
#     username = models.CharField(db_index=True, unique=True, max_length=255)
#     email = models.EmailField(unique=True)
#     date_of_birth = models.DateField()
#     profile_image = models.ImageField(upload_to="profile_images")
#     cell_phone = models.IntegerField()
#     first_name = models.CharField(max_length=50, blank=False)
#     last_name = models.CharField(max_length=50, blank=False)

#     objects = UserManager()

# USERNAME_FIELD = 'username'
# REQUIRED_FIELDS = ['email', 'cell_phone', 'first_name', 'last_name']

# def get_full_name(self):
#     return self.first_name + " " + self.last_name
