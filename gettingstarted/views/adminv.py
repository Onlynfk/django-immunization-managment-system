from django.shortcuts import render
from records.models import Record, Schedule, Vaccine
from accounts.models import  HealthCentre, MyUser

from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from django.utils.decorators import method_decorator


@login_required
@admin_required
def admin_home(request):
	all_records = Record.objects.all().count()
	all_hcs = HealthCentre.objects.all().count()
	all_schedules = Schedule.objects.all().count()
	all_hw = MyUser.objects.filter(is_hw=True).count()
	all_pho = MyUser.objects.filter(is_pho=True).count()
	all_users = MyUser.objects.all()
	list_vac = Vaccine.objects.all()
	all_hc = HealthCentre.objects.all()

	context= {
		'all_records': all_records,
		'all_schedules': all_schedules,
		'title': 'Admin',
		'all_hcs': all_hcs,
		'all_hw': all_hw,
		'all_pho': all_pho,
		'all_users':all_users,
		'list_vac': list_vac,
		'all_hc':all_hc,
	}
	return render(request, 'adminv/home.html',  context)

def charts(request):
	return render(request, 'adminv/charts.html',  {'title': 'Charts'} )

def map_data(request):
	schedules = Schedule.objects.all()

	context={
		'schedules': schedules,
		'title': 'Map Info',
	}

	return render(request, 'adminv/map_data.html', context )


def userprofiles(request):
    all_hw = MyUser.objects.filter(is_hw=True).count()
    all_pho = MyUser.objects.filter(is_pho=True).count()
    all_users = MyUser.objects.all()
    
    context= {
		'title': 'Admin',
		'all_hw': all_hw,
		'all_pho': all_pho,
		'all_users':all_users,
	}
    return render(request, 'adminv/userprofiles.html', context)
