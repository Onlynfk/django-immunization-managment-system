from django.urls import path
from .views import (records, RecordCreateView, record_detail, RecordUpdateView,
                    RecordDeleteView, ScheduleUpdateView,ScheduleDetailView, ScheduleDeleteView, VaccineCreateView, VaccineListView,
                    VaccineDetailView)

urlpatterns = [
    path('', records, name='healthw-records'),
    path('create', RecordCreateView.as_view(), name='healthw-record-create'),
    path('<int:pk>/', record_detail, name='record-detail'),
    path('<int:pk>/update/', RecordUpdateView.as_view(), name='record-update'),


    path('<int:pk>/delete/', RecordDeleteView.as_view(), name='record-delete'),\
    

    # vaccine panel
    path('vaccine/list', VaccineListView.as_view(), name='list-vaccine'),
    path('vaccine/create', VaccineCreateView.as_view(), name='add-vaccine'),
    path('vaccine/<pk>/', VaccineDetailView.as_view(), name="detail-vaccine"), 

    # schedule panel
    path('schedule/<pk>/', ScheduleDetailView.as_view(), name="schedule-detail"), 
    path('schedule/<int:pk>/update', ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedule/<int:pk>/delete', ScheduleDeleteView.as_view(), name='schedule-delete'),\
]