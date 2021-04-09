from django.shortcuts import render, redirect, get_object_or_404, reverse
from accounts.models import HealthCentre,CentreProfile
from django.views.generic import CreateView,DetailView, UpdateView,DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Record, RecordView,Schedule, Vaccine
from .forms import RecordForm,ScheduleForm, VaccineForm
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from gettingstarted.decorators import healthworker_required, phoffical_required



@method_decorator([login_required,healthworker_required ], name='dispatch')
class RecordListView(ListView):
    model = Record
    template_name = "healthw/records.html"
    context_object_name = 'records'
    
    
    
    def get_context_data(self, **kwargs):
        hw_records = "active  mt-1 mb-1"
        context = super().get_context_data(**kwargs)
        context["hw_records"] = hw_records
        context["title"] = "Your Records"
        return context 
    




@login_required
@healthworker_required
def records(request):
    if request.user.is_authenticated:
        records = Record.objects.filter(creator=request.user).order_by('created')
        page = request.GET.get('page', 1)
        paginator = Paginator(records, 2)
        #page_obj = paginator.get_page(page_number)
        print(paginator)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
    context = {
        "hw_records": "active  mt-1 mb-1",
		'records': records,
		'title': 'Your Records',
        'users': users,
    }
    return render(request, 'healthw/records.html',context)

@method_decorator([login_required,healthworker_required ], name='dispatch')
class RecordCreateView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = RecordForm
    template_name = 'healthw/create_record.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.centre = self.request.user.centreprofile.health_centre_in
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        thw_record = "active  mt-1 mb-1"
        context = super().get_context_data(**kwargs)
        context["hw_record"] = thw_record
        return context
    
    
    def get_success_url(self):
        return reverse('healthw-records')
 
@login_required
@healthworker_required
def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk)
    schedules = record.schedules.filter(active=True)
    new_schedule = None

    if request.user.is_authenticated:
        RecordView.objects.get_or_create(user=request.user, record=record)
    # Comment posted
    if request.method == 'POST':
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid(): 
            schedule_form.instance.user = request.user
            schedule_form.instance.centre = request.user.centreprofile.health_centre_in
            # Create Comment object but don't save to database yet
            new_schedule = schedule_form.save(commit=False)
            # Assign the current post to the comment
            new_schedule.record = record
            # Save the comment to the database
            new_schedule.save()
            return redirect(reverse("record-detail", kwargs={
                'pk': record.pk
            }))

    else:
        schedule_form = ScheduleForm()

    context={
        'record': record,
        'schedules': schedules,
        'new_schedule': new_schedule,
        'schedule_form': schedule_form
    }
    return render(request, 'healthw/record_detail.html', context)


@method_decorator([login_required,healthworker_required ], name='dispatch')
class RecordUpdateView(UpdateView):
    model = Record
    fields = ['first_name', 'last_name', 'birth_date', 
    'parent_name', 'parent_mobile', 'home_address', 'weight','height']
    template_name = "healthw/record_update.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        record = self.get_object()
        if self.request.user == record.creator:
            return True
        return False


@method_decorator([login_required,healthworker_required ], name='dispatch')
class RecordDeleteView(DeleteView):
    model = Record
    template_name = "healthw/record_confirm_delete.html"
    success_url = '/records/<int:pk>/'

    def test_func(self):
        record = self.get_object()
        if self.request.user == record.creator:
            return True
        return False

@method_decorator([login_required,healthworker_required ], name='dispatch')
class ScheduleUpdateView(UpdateView):
    model = Schedule
    fields = ['date_immunized','vaccine_type','exp_date','site_given',]
    template_name = "healthw/schedule_update.html"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        schedule = self.get_object()
        if self.request.user == schedule.user:
            return True
        return False

@method_decorator([login_required,healthworker_required ], name='dispatch')
class ScheduleDetailView(DetailView):
    model = Schedule
    template_name = "healthw/schedule_detail.html"

@method_decorator([login_required,healthworker_required ], name='dispatch')
class ScheduleDeleteView(DeleteView):
    model = Schedule
    template_name = "healthw/schedule_confirm_delete.html"
    
    def get_success_url(self):
        return reverse('record-detail', kwargs={'pk': self.object.record_id})  
          
    def test_func(self):
        schedule = self.get_object()
        if self.request.user == schedule.user:
            return True
        return False
    
  



class VaccineCreateView(CreateView):
    model = Vaccine
    form_class = VaccineForm
    template_name = "adminv/vaccine_create.html"
        
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('list-vaccine')

   
class VaccineDetailView(DetailView):
    model = Vaccine
    template_name = "adminv/vaccine_detail.html"
    

class VaccineListView(ListView):
    model = Vaccine
    template_name = "adminv/vaccine_list.html"
    context_object_name = 'vaccines'
 
    def get_context_data(self, **kwargs):
        thw_vaccines = "active  mt-1 mb-1"
        context = super().get_context_data(**kwargs)
        context["hw_vaccines"] = thw_vaccines
        return context

@login_required
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
    
    for entry in dataset:
        categories.append('%s Class' % entry['age_class'])
        male_series.append(entry['male'])
        female_series.append(entry['female'])

    context={
        'categories': json.dumps(categories),
        'male_series': json.dumps(male_series),
        'female_series': json.dumps(female_series)
    }
    
    return render(request, 'phealth/charts.html', context)

