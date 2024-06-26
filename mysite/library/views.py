from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def index(request):
    biblioteche = Library.objects.all()
    libri = Book.objects.all()
    membri = Member.objects.all()
    return render(request, 'home.html', {'biblioteche': biblioteche, 'libri': libri, 'membri': membri})

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
        biblioteca = request.POST['library']
        nuovo_libro = Book(book_id=id_book, title=titolo, author=autore, owned_by=biblioteca)
        nuovo_libro.save()    
    return redirect('/')

@csrf_exempt
def inserimento_membri(request):
    if request.method == 'POST':
        id_member = request.POST['member-id']
        nome = request.POST['member-name']
        biblioteca = request.POST['library']
        nuovo_membro = Member(member_id=id_member, name=nome, assigned=biblioteca)
        nuovo_membro.save()
    return redirect('/') 

def visualizza(request):
    libri = Book.objects.all()
    return render(request, 'visualizza.html', {'libri': libri})

def visualizza_biblioteche(request):
    biblioteche = Library.objects.all()
    return render(request, 'visualizza_biblioteche.html', {'biblioteche': biblioteche})

def visualizza_membri(request):
    membri = Member.objects.all()
    return render(request, 'visualizza_membri.html', {'membri': membri})

def form_borrow(request):
    if request.method == 'POST':
        member = request.POST['member']
        member = member.replace(",","")
        member_istance = Member.objects.get(member_id=member)
        biblioteca = Library.objects.filter(members=member).first() #non ritorna un cazzo non so il perchè
        print(f"{member_istance} {member_istance.assigned}")
        print(biblioteca)
    return render(request, 'form_borrow.html', {'biblioteca': biblioteca, 'member': member_istance})


def borrow_book(request):
    pass