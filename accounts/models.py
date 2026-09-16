from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
      class Role(models.TextChoices):
         BUYER = "BUYER", "Buyer"
         SELLER = "SELLER", "Seller"

      role = models.CharField(
         max_length=10,
         choices=Role.choices,
         default=Role.BUYER
      )
      
      def __str__(self):
         return f"{self.username} ({self.role})"
   
      image = models.ImageField(upload_to="avatars/", blank=True, null=True)
      phone = models.CharField(max_length=30, blank=True, null=True, help_text="+998919998877")
      address = models.CharField(max_length=255, blank=True, null=True)


