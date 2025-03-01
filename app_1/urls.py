from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('run_code/<str:problem_name>/', views.run_code, name='run_code'),
    path('problems/<str:problem_name>', views.problems, name='problems')
    ]