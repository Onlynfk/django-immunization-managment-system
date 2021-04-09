from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.models import HealthCentre,CentreProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from records.models import Record, RecordView,Schedule
from records.forms import RecordForm,ScheduleForm
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from ..decorators import healthworker_required

@login_required
@healthworker_required
def healthw_home(request):
    if request.user.is_authenticated:
        ur_records = Record.objects.filter(creator=request.user).count()
        ur_schedules = Schedule.objects.filter(user=request.user).count()
        records = Record.objects.filter(creator=request.user).all()
        c_records = Record.objects.filter(creator__centreprofile__health_centre_in=get_user_centre(request)).all()
        total_rc = Record.objects.filter(creator__centreprofile__health_centre_in=get_user_centre(request)).count()
        
    context = {
        "hw_home": "active  mt-1 mb-1",
        'ur_records': ur_records,
        'ur_schedules':ur_schedules,
        'records':records,
        'c_records':c_records,
        'total_rc':total_rc,
        'title': 'Health Worker -Admin',
    }
    return render(request, 'healthw/home.html',  context)

@login_required
@healthworker_required
def charts(request):
	return render(request, 'healthw/charts.html',  {'title': 'Charts'} )



def get_user_centre(request):
    if request.user.is_authenticated and request.user.is_hw:
        user_centre = request.user.centreprofile.health_centre_in.id
        return user_centre

@login_required
@healthworker_required
def centre(request):
    records = Record.objects.filter(creator__centreprofile__health_centre_in=get_user_centre(request))
    total_rc = Record.objects.filter(creator__centreprofile__health_centre_in=get_user_centre(request)).count()

    context = {
        "hwcentre": "active  mt-1 mb-1",
        'records': records,
        'total_rc': total_rc,
        'title': 'Records',
    }
    return render(request, 'healthw/centre_updates.html', context)
