from django.urls import path

from . import views

urlpatterns = [
    path('send_emails/', views.send_emails, name='send_emails'),
    path('employee/<int:pk>', views.employee, name='employees'),
    path('employees/', views.employees, ),
    path('events/', views.events, name='events'),
    path('email_logs/', views.email_logs, name='email_logs'),
    path('templates/', views.templates, name='templates'),

]