from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import MyUser, CentreProfile, OfficailProfile, HealthCentre, Lga, State
from django.utils.safestring import mark_safe

GENDER_CHOICES = ((1, 'Male'), (0, 'Female'))   

class CentreRegForm(UserCreationForm):
    username = forms.CharField(label='User Name')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Surname')
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES)
    health_centre_in = forms.ModelChoiceField(queryset=HealthCentre.objects.all(), initial=0, label="Health Centre")
    lga = forms.ModelChoiceField(queryset=Lga.objects.all(), initial=0, label=" LGA")
    state = forms.ModelChoiceField(queryset=State.objects.all(), initial=0, label=" states")
    phone_number = forms.CharField(label='Phone Number')

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['username', 'first_name','last_name','state','lga',
                'email', 'gender', 'health_centre_in','phone_number','password1','password2']
    
   
    @transaction.atomic
    def save(self): 
        user = super().save(commit=False)
        user.is_hw = True
        user.save()
        p = CentreProfile.objects.create(user=user)
        p.email = self.cleaned_data.get('email')
        p.gender = self.cleaned_data.get('gender')
        p.health_centre_in = self.cleaned_data.get('health_centre_in')
        p.phone_number = self.cleaned_data.get('phone_number')
        p.save()
        return user



class OfficialRegForm(UserCreationForm):
    username = forms.CharField(label='User Name')
    email = forms.CharField(label='Email')
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES)


    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['username','email', 'gender','password1','password2']

    
    @transaction.atomic
    def save(self): 
        user = super().save(commit=False)
        user.is_pho = True
        user.save()
        p = OfficailProfile.objects.create(user=user)
        p.email = self.cleaned_data.get('email')
        p.gender = self.cleaned_data.get('gender')
        p.save()
        return user

















