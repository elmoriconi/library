from django.db import models

class Book(models.Model):
    book_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_borrowed = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book_id}, {self.title}, {self.author}, {self.is_borrowed}"

class Member(models.Model):
    member_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    borrowed_books = models.ManyToManyField(Book)

    def __str__(self):
        return f"{self.member_id}, {self.name}, {self.borrowed_books}"

class Library(models.Model):
    books = models.ManyToManyField(Book)
    members = models.ManyToManyField(Member)

    def add_book(self, book_id, title, author):
        book = Book.objects.create(book_id=book_id, title=title, author=author)
        self.books.add(book)

    def register_member(self, member_id, name):
        member = Member.objects.create(member_id=member_id, name=name)
        self.members.add(member)

    def borrow_book(self, member_id, book_id):
        book = Book.objects.get(book_id=book_id)
        member = Member.objects.get(member_id=member_id)
        member.borrowed_books.add(book)

    def return_book(self, member_id, book_id):
        book = Book.objects.get(book_id=book_id)
        member = Member.objects.get(member_id=member_id)
        member.borrowed_books.remove(book)

    def get_borrowed_books(self, member_id):
        member = Member.objects.get(member_id=member_id)
        return member.borrowed_books.all()