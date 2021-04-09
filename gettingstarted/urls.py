from django.urls import path, include

from django.contrib import admin

from django.contrib.auth import views as auth_views

from gettingstarted.views import hw, pho, main, doctor, adminv

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    
    
    # admin panel
    path('panel-admin/', adminv.admin_home, name='admin-home'),
    path('charts/', adminv.charts, name='admin-charts'),
    path('map-data/', adminv.map_data, name='admin-map-data'),
    
    #all
    path('accounts/profile/', main.profile, name='main-profile'),
    # path('user/profiles/', adminv.userprofiles, name='user-profiles'),

    # healthworker panel
    path('dashboard-hw/', hw.healthw_home, name='healthw-home'),
    path('centre-hw/', hw.centre, name='healthw-centre'),
    path('records/', include('records.urls')),
        
    
    # public health offical
    path('dashboard-ho/', pho.phealth_home, name='phealth-home'),
    path('mapview-ho/', pho.mapview, name='phealth-maps'),
    path('all-records/', pho.all_records.as_view(), name="all-centre-records"),
    path('hc-charts/',pho.RecordChart , name="hc-charts"),
    path('hc-tables/',pho.tables , name="hc-tables"),

    #main home
    path('', main.home_page, name='main-home')
    

]