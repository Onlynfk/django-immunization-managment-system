from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class MyUser(AbstractUser):
    is_hw = models.BooleanField(default=False)
    is_pho = models.BooleanField(default=False)



GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)


class CentreProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    health_centre_in = models.ForeignKey('HealthCentre', on_delete=models.CASCADE, related_name='centre', blank=True, null=True)


    def __str__(self):
        return self.user.username
 

class OfficailProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.CharField(max_length=100)
    status = models.ForeignKey('PlaceStatus', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.user.username


# adding health centre tables
class HealthCentre(models.Model):                                                  
    name = models.CharField(max_length=100, blank=True, null=True)
    full_address = models.CharField(max_length=500) 
    latitude = models.CharField(max_length=60)
    longitude = models.CharField(max_length=60)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    local = models.ForeignKey('Lga', on_delete=models.CASCADE)
    status = models.ForeignKey('PlaceStatus', on_delete=models.CASCADE, blank=True, null=True)

    
    def __str__(self):
        return self.name


class State(models.Model):
    name  = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self    ):
        return self.name

class Lga(models.Model):
    local  = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.local


class PlaceStatus(models.Model):
    status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Place statuses"
    
    def __unicode__(self):
        return self.status

    def __str__(self):
        return self.status

