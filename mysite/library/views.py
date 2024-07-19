from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def index(request):
    biblioteche = Library.objects.all()
    libri = Book.objects.all()
    membri = Member.objects.all()
    libri_modificabili = Book.objects.filter(is_borrowed=False)
    return render(request, 'home.html', {'biblioteche': biblioteche, 'libri': libri, 'membri': membri, 'libri_modificabili': libri_modificabili})

def create_library(request):
    try:
        if request.method == 'POST':
            library = request.POST['libraryname']
            library = library.replace(" ", "_")
            new_library = Library.objects.create(name=library)
            new_library.save()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:
        return redirect('/')

@csrf_exempt
def inserimento(request):
    try:
        if request.method == 'POST':
            id_book = request.POST['book-id']
            titolo = request.POST['book-title']
            autore = request.POST['book-author']
            biblioteca = request.POST['library']
            biblioteca_agg = Library.objects.get(name=biblioteca)
            nuovo_libro = Book.objects.create(book_id=id_book, title=titolo, author=autore, owned_by=biblioteca_agg)
            nuovo_libro.save()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:  
        return redirect('/')
    
def form_modify_book(request):
    try:
        if request.method == 'POST':
            book = request.POST['book']
            book_istance = Book.objects.get(book_id=book)
            if book_istance.is_borrowed:
                return redirect('/')
            biblioteche = Library.objects.all()
            return render(request, 'form_modify_book.html', {'book': book_istance, 'biblioteche': biblioteche})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

@csrf_exempt
def modify_book(request):
    try:
        if request.method == 'POST':
            book = request.POST['book']
            book_istance = Book.objects.get(book_id=book)
            title = request.POST['title']
            author = request.POST['author']
            library = request.POST['library']
            if title:
                book_istance.title = title
            if author:
                book_istance.author = author
            if not(library == "None"):
                library_istance = Library.objects.get(name=library)
                book_istance.owned_by = library_istance
            book_istance.save()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:
        return redirect('/')

@csrf_exempt
def inserimento_membri(request):
    try:
        if request.method == 'POST':
            id_member = request.POST['member-id']
            nome = request.POST['member-name']
            biblioteca = request.POST['library']
            biblioteca_agg = Library.objects.get(name=biblioteca)
            nuovo_membro = Member.objects.create(member_id=id_member, name=nome, assigned=biblioteca_agg)
            nuovo_membro.save()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:
        return redirect('/') 

def visualizza(request):
    try:
        libri = Book.objects.all()
        return render(request, 'visualizza.html', {'libri': libri})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')
    
def visualizza_specifica_libro(request):
    try:
        if request.method == 'POST':
            return render(request, 'visualizza_specifica_libro.html', {'libro': Book.objects.get(book_id=request.POST['book'])})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')
    
def elimina_libro(request):
    try:
        if request.method == 'POST':
            book_istance = Book.objects.get(book_id=request.POST['book'])
            if not book_istance.is_borrowed:
                book_istance.delete()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:
        return redirect('/')

def visualizza_biblioteche(request):
    try:
        biblioteche = Library.objects.all()
        return render(request, 'visualizza_biblioteche.html', {'biblioteche': biblioteche})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

def visualizza_membri(request):
    try:
        membri = Member.objects.all()
        return render(request, 'visualizza_membri.html', {'membri': membri})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

def form_modify_member(request):
    try:
        if request.method == 'POST':
            member = request.POST['member']
            member = Member.objects.get(member_id=member)
            books = Book.objects.filter(borrowed_by=member)
            if books:
                return redirect('/')
        return render(request, 'form_modify_member.html', {'member': member, 'biblioteche': Library.objects.all()})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

@csrf_exempt
def modify_member(request):
    try:
        if request.method == 'POST':
            member = Member.objects.get(member_id=request.POST['member'])
            name = request.POST['name']
            library = request.POST['library']
            if name:
                member.name = name
            if not(library == "None"):
                library_istance = Library.objects.get(name=library)
                member.assigned = library_istance
            member.save()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:
        return redirect('/')
    
def elimina_membro(request):
    try:
        if request.method == 'POST':
            member = Member.objects.get(member_id=request.POST['member'])
            books = Book.objects.filter(borrowed_by=member)
            if books:
                return redirect('/')
            member.delete()
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
    finally:
        return redirect('/')
    
def form_borrow(request):
    try:
        if request.method == 'POST':
            member = request.POST['member']
            member_istance = Member.objects.get(member_id=member)
            biblioteca = Library.objects.get(name=member_istance.assigned.name)
            libri_biblioteca = Book.objects.filter(owned_by=biblioteca.name, is_borrowed=False)
        return render(request, 'form_borrow.html', {'library': biblioteca, 'member': member_istance, 'books': libri_biblioteca})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

def borrow_book(request):
    try:
        if request.method == 'POST':
            book = request.POST['prestito']
            member = request.POST['member']
            book_istance = Book.objects.get(book_id=book)
            member_istance = Member.objects.get(member_id=member)
            book_istance.borrow(member_istance)
        return redirect(index(request))
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

def form_return(request):
    try:
        if request.method == 'POST':
            member = request.POST['member']
            member_istance = Member.objects.get(member_id=member)
            biblioteca = Library.objects.get(name=member_istance.assigned.name)
            libri_biblioteca = Book.objects.filter(owned_by=biblioteca.name, is_borrowed=True, borrowed_by=member_istance)
        return render(request, 'form_return.html', {'library': biblioteca, 'member': member_istance, 'books': libri_biblioteca})
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')

def return_book(request):
    try:
        if request.method == 'POST':
            book = request.POST['prestito']
            book_istance = Book.objects.get(book_id=book)
            book_istance.giveBack()
        return redirect(index(request))
    except Exception as e:
        print(f"Something has gone wrong\n{e}")
        return redirect('/')
    
def function_books(request):
    if request.method == 'POST':
        if request.POST['type'] == 'modify':
            return form_modify_book(request)
        elif request.POST['type'] == 'read':
            return visualizza_specifica_libro(request)
        elif request.POST['type'] == 'delete':
            return elimina_libro(request)
        else:
            print('Errore')
        return redirect('/')
    
def function_member(request):
    if request.method == 'POST':
        if request.POST['type'] == 'modify':
            return form_modify_member(request)
        elif request.POST['type'] == 'delete':
            return elimina_membro(request)
        elif request.POST['type'] == 'borrow':
            return form_borrow(request)
        elif request.POST['type'] == 'return':
            return form_return(request)
        else:
            print('Errore')
        return redirect('/')