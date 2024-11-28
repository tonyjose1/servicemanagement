# employee/urls.py
from django.urls import path
from . import views

app_name = 'employee'  # This sets the namespace for the app

urlpatterns = [
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('view_worksite/<int:work_id>/', views.view_worksite, name='view_worksite'),
    path('update_work/<int:work_id>/', views.update_work, name='update_work'),
    path('talk_to_admin/<int:work_id>/', views.talk_to_admin, name='talk_to_admin'),
]
