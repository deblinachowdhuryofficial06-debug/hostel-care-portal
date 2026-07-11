from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_portal, name='home_portal'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # New Split Registration Paths
    path('register/student/', views.student_register, name='register_student'),
    path('register/warden/', views.warden_register, name='register_warden'),
    
    # Dashboards & Actions
    path('student/dashboard/', views.student_dashboard, name='dashboard'),
    path('create/', views.create_complaint, name='create_complaint'),
    path('delete/<int:pk>/', views.delete_complaint, name='delete_complaint'),
    path('warden/', views.warden_dashboard, name='warden_dashboard'),
    path('status/<int:pk>/<str:new_status>/', views.update_status, name='update_status'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
]