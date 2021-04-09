
import json
from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.models import HealthCentre,CentreProfile, MyUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  TemplateView
from records.models import Record, RecordView,Schedule, Vaccine
from records.forms import RecordForm,ScheduleForm
from django.utils import timezone
from django.db.models import Count, Q
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from ..decorators import phoffical_required
from django.utils.decorators import method_decorator



@phoffical_required
def phealth_home(request):
	all_records = Record.objects.all().count()
	all_hc = HealthCentre.objects.all().count()
	all_schedules = Schedule.objects.all().count()
	hcs = HealthCentre.objects.all()
	all_hw = MyUser.objects.filter(is_hw=True).count()
	all_phw = MyUser.objects.filter(is_pho=True).count()
	qs = Vaccine.objects.all()


	context= {
		'all_hc':all_hc,
		'all_records': all_records,
		'all_schedules': all_schedules,
		'hcs':hcs,
		'all_hw':all_hw,
		'all_phw': all_phw,
		'qs':qs,
		'title': 'Health Official Admin',

	}
	return render(request, 'phealth/home.html', context)




@method_decorator([login_required,phoffical_required ], name='dispatch')
class all_records(ListView):
    model = Record
    context_object_name = 'records'
    template_name = "phealth/all_records.html"
    ordering = ['-created']
    paginate_by = 4

      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hc"] = HealthCentre.objects.all()
        context["title"] = "All Centre Records"
        context["total_rc"] = Record.objects.all().count()
        return context

@phoffical_required
def RecordChart(request):
    dataset = Record.objects \
        .values('age_class') \
        .annotate(male=Count('age_class', filter=Q(gender="M")),
                  female=Count('age_class', filter=Q(gender="F"))) \
        .order_by('age_class')
    print(dataset)
    
    categories = list()
    male_series = list()
    female_series = list()
    vacs = Vaccine.objects.all()
    
    for entry in dataset:
        categories.append('%s Class' % entry['age_class'])
        male_series.append(entry['male'])
        female_series.append(entry['female'])
        
    
    
    context={
		'vacs':vacs,
		'categories': json.dumps(categories),
        'male_series': json.dumps(male_series),
        'female_series': json.dumps(female_series)
    }
    return render(request, template_name='phealth/charts.html', context=context)


@phoffical_required
def tables(request):
	hcs = HealthCentre.objects.all()
	records = Record.objects.all()
	all_hw = MyUser.objects.filter(is_hw=True).count()
	all_phw = MyUser.objects.filter(is_pho=True).count()

	context={
		'records': records,
		'hcs':hcs,
		'all_hw':all_hw,
		'all_phw': all_phw,
		'title': 'Tables',
	}

	return render(request, 'phealth/tables.html',  context)

def default_map(request):
    mapbox_access_token = 'pk.eyJ1Ijoib25seW5mayIsImEiOiJja2J4dDhrdnUwdDd6MnF0Ym1qZGVtY2w5In0.Cc7OeIVzjmoCpQEnMmx8-w'
    return render(request, 'maps/map.html')




@phoffical_required
def mapview(request):
    primary_centres= HealthCentre.objects.filter(status_id=3).order_by('name')
    federal_centres = HealthCentre.objects.filter(status_id=1).order_by('name')
    if 'LANGUAGE_CODE' in request.COOKIES:
        language_code = request.COOKIES.get('LANGUAGE_CODE')
    else:
        language_code = 'en'            

    return render(request, 'phealth/map.html',
                  {'primary_centres': primary_centres,
                   'federal_centres': federal_centres, 
                   'LANGUAGE_CODE': language_code,
                   'title': 'Maps',})
