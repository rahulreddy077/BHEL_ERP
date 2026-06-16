from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('finance/', views.finance_module, name='finance_module'),
    path('module/<str:module_name>/', views.module_detail, name='module_detail'),
]