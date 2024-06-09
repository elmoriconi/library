from django.urls import *
from . import views

urlpatterns = [
    path('inserimento/', views.inserimento, name='inserimento'),
    path("", views.index, name="index"),
    path('visualizza/', views.visualizza, name='visualizza')
]
