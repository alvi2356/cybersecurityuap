from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('achievements/', views.achievements, name='achievements'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

]