from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('report/', views.report_case, name='report_case'),
    path('voice-report/', views.voice_report, name='voice_report'),
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    path('stations/', views.station_finder, name='station_finder'),
    path('safety-tips/', views.safety_tips, name='safety_tips'),
    path('notifications/', views.notifications_view, name='notifications'),
]