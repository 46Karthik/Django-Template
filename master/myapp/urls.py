from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('crm/', CRMView.as_view(), name='crm'),
    path('crm/<int:id>/', CRMView.as_view(), name='crm'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

