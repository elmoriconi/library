from django.urls import *
from . import views

urlpatterns = [
    path('inserimento/', views.inserimento, name='inserimento'),
    path("", views.index, name="index"),
    path('visualizza/', views.visualizza, name='visualizza'),
    path('create_library/', views.create_library, name='create_library' ),
    path('visualizza_biblioteche/', views.visualizza_biblioteche, name='visualizza_biblioteche'),
    path('visualizza_membri/', views.visualizza_membri, name='visualizza_membri'),
    path('inserimento_membri/', views.inserimento_membri, name='inserimento_membri'),
    path('form_borrow/', views.form_borrow, name='form_borrow'),
    path('borrow_book/', views.borrow_book, name='borrow_book'),
    path('form_return/', views.form_return, name='form_return'),
    path('return_book/', views.return_book, name='return_book'),
    path('modify_book/', views.modify_book, name='modify_book'),
    path('form_modify_book/', views.form_modify_book, name='form_modify_book'),
    path('modify_book/', views.modify_book, name='modify_book'),
    path('visualizza_specifica_libro/', views.visualizza_specifica_libro, name='visualizza_specifica_libro'),
    path('elimina_libro/', views.elimina_libro, name='elimina_libro'),
    path('form_modify_member/', views.form_modify_member, name='form_modify_member'),
    path('modify_member/', views.modify_member, name='modify_member'),
    path('elimina_membro/', views.elimina_membro, name='elimina_membro'),
    path('function_books/', views.function_books, name='function_books'),
    path('function_member/', views.function_member, name='function_member'),
    path('home/', views.home, name='home')
]
