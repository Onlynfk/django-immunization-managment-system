# records
from django.db import models
from django.urls import reverse
from django.utils import timezone
from accounts.models import MyUser, HealthCentre
from django.contrib.auth import get_user_model


User = get_user_model()



class RecordView(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    record = models.ForeignKey('Record', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

TIME = (
    ('B', 'Birth'),
    ('6w', '6 weeks (Infants)'),
    ('10w', '10 weeks (Infants)'),
    ('14w', '14 weeks (Infants)'),
    ('6m', '6 moonths (Infants)'),
    ('9m', '9 months (Infants)'),
    ('12m', '12-24 months (Infants)'),
    ('15m', '15-18 months (Infants)'),
    ('24m', '24 months (Infants)'),
    ('L', 'Less than 13 years '),
)



class Timing(models.Model):
    title = models.CharField(max_length=200)
    age = models.CharField(max_length=30)
    schedule_done = models.ForeignKey('Schedule', related_name='schedules_done', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return 


class Immunogen(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    definition = models.CharField(max_length=100, blank=True, null=True)
    disease_handled = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.definition

    def __unicode__(self):
        return 

class Vaccine(models.Model):
    timing = models.CharField(max_length=20, choices=TIME)
    imu_id = models.ForeignKey('Immunogen', related_name='imus', on_delete=models.CASCADE)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.imu_id.definition

    def get_absolute_url(self):
        return reverse('detail-vaccine', kwargs={
            'pk': self.pk
        })

    @property
    def usage(self):
        return self.schedule_set.count()

SITE = (
    ('L', 'Left Arm'),
    ('R', 'Right Arm')
)

   
class Schedule(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    centre = models.ForeignKey(HealthCentre, on_delete=models.CASCADE, related_name='sch_centres', blank=True, null=True)
    record = models.ForeignKey('Record', related_name='schedules', on_delete=models.CASCADE)
    date_immunized = models.DateTimeField(default=timezone.now)
    vaccine_type = models.ForeignKey('Vaccine', related_name='vaccines', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    exp_date = models.DateTimeField(blank=True, null=True)
    site_given = models.CharField(max_length=12, choices=SITE, blank=True, null=True)

    
    def __str__(self):
        return self.vaccine_type.imu_id.name
    
    def get_update_url(self):
        return reverse('schedule-update', kwargs={
            'pk': self.pk
        })
    def get_absolute_url(self):
        return reverse('schedule-detail', kwargs={
            'pk': self.pk
        })
    
    
    def get_delete_url(self):
        return reverse('schedule-delete', kwargs={
            'pk': self.pk
        })


GENDER_CHOICES =( 
    ("M", "Male"),
    ("F", "Female"),
    
) 
class Record(models.Model):
    creator = models.ForeignKey(MyUser, related_name='user', on_delete=models.CASCADE)
    centre = models.ForeignKey(HealthCentre, on_delete=models.CASCADE, related_name='rec_centres', blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    parent_name = models.CharField(max_length=50, blank=True, null=True)
    parent_mobile = models.CharField(max_length=50, blank=True, null=True)
    home_address = models.CharField(max_length=300, blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    age_class = models.PositiveSmallIntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    
    @property
    def usage(self):
        return self.schedule_set.count()

   
    def get_absolute_url(self):
        return reverse('record-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('record-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('record-delete', kwargs={
            'pk': self.pk
        })

    




