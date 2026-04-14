from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    # User URLs
    path('', views.dashboard, name='dashboard'),
    path('report/', views.report_case, name='report_case'),
    path('voice-report/', views.voice_report, name='voice_report'),
    path('case/<int:case_id>/', views.case_detail, name='case_detail'),
    path('stations/', views.station_finder, name='station_finder'),
    path('safety-tips/', views.safety_tips, name='safety_tips'),
    path('notifications/', views.notifications_view, name='notifications'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/case/<int:case_id>/', views.admin_case_detail, name='admin_case_detail'),
    path('admin/assign/<int:case_id>/', views.assign_case, name='assign_case'),
]