from django.contrib import admin 
# from django.contrib.auth.admin import UserAdmin
from django.contrib import auth
from .models import OfficailProfile, CentreProfile, MyUser, HealthCentre, State, Lga, PlaceStatus




class MyUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(MyUser, MyUserAdmin)












class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id','status')

admin.site.register(PlaceStatus, PlaceAdmin)


class StateAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    #list_display =  [field.name for field in State._meta.fields if field.name != "id"]

admin.site.register(State, StateAdmin)

admin.site.register(Lga)
# admin.site.register(CentreProfile)
# admin.site.register(OfficailProfile)
admin.site.register(HealthCentre)
#admin.site.register(State)
#admin.site.register(Lga)