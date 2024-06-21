from django.urls import *
from . import views

urlpatterns = [
    path('inserimento/', views.inserimento, name='inserimento'),
    path("", views.index, name="index"),
    path('visualizza/', views.visualizza, name='visualizza'),
    path('create_library/', views.create_library, name='create_library' ),
    path('visualizza_biblioteche/', views.visualizza_biblioteche, name='visualizza_biblioteche')
]
