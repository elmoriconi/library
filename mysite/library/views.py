from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def index(request):
    biblioteche = Library.objects.all()
    return render(request, 'home.html', {'biblioteche': biblioteche})

def create_library(request):
    if request.method == 'POST':
        library = request.POST['libraryname']
        new_library = Library(name=library)
        new_library.save()
        return redirect('/')
    return render(request, 'create_library.html')

@csrf_exempt
def inserimento(request):
    if request.method == 'POST':
        id_book = request.POST['book-id']
        titolo = request.POST['book-title']
        autore = request.POST['book-author']
        
        # Inserimento nel database
        nuovo_libro = Book(book_id=id_book, title=titolo, author=autore)
        nuovo_libro.save()
        
        return redirect('/')
    
    return render(request, 'inserimento.html')

def visualizza(request):
    libri = Book.objects.all()
    return render(request, 'visualizza.html', {'libri': libri})

def visualizza_biblioteche(request):
    biblioteche = Library.objects.all()
    return render(request, 'visualizza_biblioteche.html', {'biblioteche': biblioteche})
