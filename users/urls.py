from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('admin-profile/', views.AdminProfileView.as_view()),
    path('employer-profile/', views.EmployerProfileView.as_view()),
    path('applicant-profile/', views.ApplicantProfileView.as_view()),
]

