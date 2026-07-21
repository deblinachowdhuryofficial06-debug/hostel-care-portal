from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_portal, name='home_portal'),
    path('student/dashboard/', views.dashboard, name='dashboard'),
    path('warden/dashboard/', views.warden_dashboard, name='warden_dashboard'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/warden/', views.register_warden, name='register_warden'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('complaint/create/', views.create_complaint, name='create_complaint'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:pk>/status/', views.update_status, name='update_status'),
]