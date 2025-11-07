from django.urls import path
#from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('inventory/', views.inventory_view, name='inventory'),
    path('generate-bill/', views.generate_bill, name='generate_bill'),
    path('bill-details/<int:bill_id>/', views.bill_details, name='bill_details'),
    path('download-pdf/<int:bill_id>/', views.download_pdf, name='download_pdf'),
    path('bill-history/', views.bill_history, name='bill_history'),
    path('bill-success/', views.bill_success, name='bill_success_page'),
    path('accounts/login/', views.login_view, name='login'),
    path('edit/<int:pk>/', views.edit_medicine, name='edit_medicine'),
    path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'),
    path('add/', views.add_medicine, name='add_medicine'),

]
