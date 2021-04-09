from django.shortcuts import render
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from .models import MyUser,Lga,State
from .forms import CentreRegForm, OfficialRegForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from gettingstarted.decorators import admin_required
from django.utils.decorators import method_decorator



@method_decorator([login_required,admin_required ], name='dispatch')
class CentreRegView(CreateView):
    model = MyUser
    form_class = CentreRegForm
    template_name = 'adminv/create_users.html'


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = ' Health Worker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'New user was added successfully!')  # <-
        return redirect('hw_signup')

    
@method_decorator([login_required,admin_required ], name='dispatch')
class OfficialRegView(CreateView):
    model = MyUser
    form_class = OfficialRegForm
    template_name = 'adminv/create_users.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Public Official'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'New user was added successfully!')  # <-
        return redirect('pho_signup')

# AJAX
def load_lgas(request):
    state_id = request.GET.get('state_id')
    lgas = Lga.objects.filter(state_id=state_id).all()
    return render(request, 'lga/drop.html', {'lgas': lgas})
