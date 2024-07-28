from django.test import TestCase, Client
from django.urls import reverse
from .models import Library, Book, Member
from django.views.decorators.csrf import csrf_exempt

class LibraryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.library_name = "Test_Library"
        self.library = Library.objects.create(name=self.library_name)
        
        self.book_id = "12345"
        self.book_title = "Test Book"
        self.book_author = "Test Author"
        self.book = Book.objects.create(book_id=self.book_id, title=self.book_title, author=self.book_author, owned_by=self.library, is_borrowed=False)
        
        self.member_id = "123"
        self.member_name = "Test Member"
        self.member = Member.objects.create(member_id=self.member_id, name=self.member_name, assigned=self.library)

    def test_form_modify_book(self):
        response = self.client.post(reverse('form_modify_book'), {'book': self.book_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_modify_book.html')
        self.assertEqual(response.context['book'].book_id, self.book_id)
        self.assertEqual(len(response.context['biblioteche']), 1)

    def test_form_modify_book_borrowed(self):
        self.book.is_borrowed = True
        self.book.save()
        response = self.client.post(reverse('form_modify_book'), {'book': self.book_id})
        self.assertEqual(response.status_code, 302)

    @csrf_exempt
    def test_modify_book(self):
        new_library = Library.objects.create(name="Another_Library")
        response = self.client.post(reverse('modify_book'), {
            'book': self.book_id,
            'title': 'Modified Book Title',
            'author': 'Modified Author',
            'library': new_library.name
        })
        self.assertEqual(response.status_code, 302)
        modified_book = Book.objects.get(book_id=self.book_id)
        self.assertEqual(modified_book.title, 'Modified Book Title')
        self.assertEqual(modified_book.author, 'Modified Author')
        self.assertEqual(modified_book.owned_by, new_library)

    @csrf_exempt
    def test_inserimento_membri(self):
        new_library = Library.objects.create(name="Another_Library")
        response = self.client.post(reverse('inserimento_membri'), {
            'member-id': '456',
            'member-name': 'New Member',
            'library': new_library.name
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Member.objects.filter(member_id='456').exists())

    def test_visualizza(self):
        response = self.client.get(reverse('visualizza'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualizza.html')
        self.assertEqual(len(response.context['libri']), 1)

    def test_visualizza_specifica_libro(self):
        response = self.client.post(reverse('visualizza_specifica_libro'), {'book': self.book_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualizza_specifica_libro.html')
        self.assertEqual(response.context['libro'].book_id, self.book_id)

    def test_elimina_libro(self):
        response = self.client.post(reverse('elimina_libro'), {'book': self.book_id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(book_id=self.book_id).exists())

    def test_elimina_libro_borrowed(self):
        self.book.is_borrowed = True
        self.book.save()
        response = self.client.post(reverse('elimina_libro'), {'book': self.book_id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(book_id=self.book_id).exists())

    def test_visualizza_biblioteche(self):
        response = self.client.get(reverse('visualizza_biblioteche'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualizza_biblioteche.html')
        self.assertEqual(len(response.context['biblioteche']), 1)

    def test_visualizza_membri(self):
        response = self.client.get(reverse('visualizza_membri'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualizza_membri.html')
        self.assertEqual(len(response.context['membri']), 1)

    def test_form_modify_member(self):
        response = self.client.post(reverse('form_modify_member'), {'member': self.member_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_modify_member.html')
        self.assertEqual(response.context['member'].member_id, self.member_id)

    def test_form_modify_member_with_books(self):
        self.book.borrow(self.member)
        response = self.client.post(reverse('form_modify_member'), {'member': self.member_id})
        self.assertEqual(response.status_code, 302)

    @csrf_exempt
    def test_modify_member(self):
        new_library = Library.objects.create(name="Another_Library")
        response = self.client.post(reverse('modify_member'), {
            'member': self.member_id,
            'name': 'Modified Member Name',
            'library': new_library.name
        })
        self.assertEqual(response.status_code, 302)
        modified_member = Member.objects.get(member_id=self.member_id)
        self.assertEqual(modified_member.name, 'Modified Member Name')
        self.assertEqual(modified_member.assigned, new_library)

    def test_elimina_membro(self):
        response = self.client.post(reverse('elimina_membro'), {'member': self.member_id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Member.objects.filter(member_id=self.member_id).exists())

    def test_elimina_membro_with_books(self):
        self.book.borrow(self.member)
        response = self.client.post(reverse('elimina_membro'), {'member': self.member_id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Member.objects.filter(member_id=self.member_id).exists())

    def test_form_borrow(self):
        response = self.client.post(reverse('form_borrow'), {'member': self.member_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_borrow.html')
        self.assertEqual(response.context['member'].member_id, self.member_id)
        self.assertEqual(response.context['library'].name, self.library_name)
        self.assertEqual(len(response.context['books']), 1)

    def test_borrow_book(self):
        response = self.client.post(reverse('borrow_book'), {'prestito': self.book_id, 'member': self.member_id})
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.borrowed_by, self.member)
        self.assertTrue(self.book.is_borrowed)

    def test_form_return(self):
        self.book.borrow(self.member)
        response = self.client.post(reverse('form_return'), {'member': self.member_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_return.html')
        self.assertEqual(response.context['member'].member_id, self.member_id)
        self.assertEqual(response.context['library'].name, self.library_name)
        self.assertEqual(len(response.context['books']), 1)

    def test_return_book(self):
        self.book.borrow(self.member)
        response = self.client.post(reverse('return_book'), {'prestito': self.book_id})
        self.assertEqual(response.status_code, 302)
        self.book.refresh_from_db()
        self.assertIsNone(self.book.borrowed_by)
        self.assertFalse(self.book.is_borrowed)

    def test_function_books_modify(self):
        response = self.client.post(reverse('function_books'), {'type': 'modify', 'book': self.book_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_modify_book.html')

    def test_function_books_read(self):
        response = self.client.post(reverse('function_books'), {'type': 'read', 'book': self.book_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'visualizza_specifica_libro.html')

    def test_function_books_delete(self):
        response = self.client.post(reverse('function_books'), {'type': 'delete', 'book': self.book_id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(book_id=self.book_id).exists())

    def test_function_member_modify(self):
        response = self.client.post(reverse('function_member'), {'type': 'modify', 'member': self.member_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_modify_member.html')

    def test_function_member_delete(self):
        response = self.client.post(reverse('function_member'), {'type': 'delete', 'member': self.member_id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Member.objects.filter(member_id=self.member_id).exists())

    def test_function_member_borrow(self):
        response = self.client.post(reverse('function_member'), {'type': 'borrow', 'member': self.member_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_borrow.html')

    def test_function_member_return(self):
        self.book.borrow(self.member)
        response = self.client.post(reverse('function_member'), {'type': 'return', 'member': self.member_id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_return.html')