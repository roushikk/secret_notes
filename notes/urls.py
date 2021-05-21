from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('created/', views.created, name='created'),
    path('<slug:slug>/', views.note, name='note'),
]
