from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_requisition, name='create_requisition'),
    path('requisition/<int:pk>/', views.requisition_detail, name='requisition_detail'),
    path('requisition/<int:pk>/approve/', views.approve_requisition, name='approve_requisition'),
]
