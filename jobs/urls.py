from django.urls import path
from .import views

urlpatterns = [
    path('employer/', views.EmployerView.as_view()),
    path('employer/<str:id>/', views.EmployerDetailView.as_view()),
    path('applicants/', views.ApplicantsView.as_view()),
    path('applicants/<str:id>/', views.ApplicantsDetailView.as_view()),
    path('jobs/', views.JobsView.as_view()),
    path('jobs/<str:id>/', views.JobsDetailView.as_view()),
    path('application/', views.ApplicationView.as_view()),
    path('application/<str:id>/', views.ApplicationDetailView.as_view()),

]

