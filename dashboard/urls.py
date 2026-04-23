"""
URL configuration for the dashboard app.
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardOverviewView.as_view(), name='overview'),
    path('listings/', views.MyListingsView.as_view(), name='listings'),
    path('inbox/', views.MyInboxView.as_view(), name='inbox'),
  
]
