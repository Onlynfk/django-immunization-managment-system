from django.urls import path
from .views import CentreRegView, OfficialRegView,load_lgas
from gettingstarted.views import main
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    # health worker
    path('create/hw', CentreRegView.as_view(), name='hw_signup'),
    

    
    # public health worker
    path('create/phw', OfficialRegView.as_view(), name='pho_signup'),
    
    # main
    path('login/', main.user_login, name='login'),
    path('logout/', main.user_logout, name='logout'),
    
    path('password/change/',auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html'),
        name='password_change'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')), name='password_change_done'),

    
    # load lga
    path('ajax/load-lga/', load_lgas, name='ajax_load_lgas'), # AJAX

]
