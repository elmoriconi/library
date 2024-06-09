from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def index(request):
    
    return render(request, 'home.html')

@csrf_exempt
def inserimento(request):
    if request.method == 'POST':
        id_book = request.POST['book-id']
        titolo = request.POST['book-title']
        autore = request.POST['book-author']
        
        # Inserimento nel database
        nuovo_libro = Book(book_id=id_book, titolo=titolo, autore=autore)
        nuovo_libro.save()
        
        return redirect('/')
    
    return render(request, 'inserimento.html')
