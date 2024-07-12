from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100, default = None, unique = True, primary_key=True)

    """def add_library(self, name):
        library = Library.objects.create(name)
        library.save()

    def add_book(self, book_id, title, author, library):
        book = Book.objects.create(book_id=book_id, title=title, author=author)
        self.library = library
        book.save()
        self.books.add(book)

    def register_member(self, member_id, name, library):
        member = Member.objects.create(member_id=member_id, name=name)
        self.library = library
        member.save()
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
    
    @staticmethod
    def get_library_of_member(member_id):
        member = Member.objects.get(member_id=member_id)
        library = Library.objects.filter(members=member).first()
        return library"""

class Member(models.Model):
    member_id = models.CharField(max_length=100, default = None)
    name = models.CharField(max_length=100, default = None)
    assigned = models.ForeignKey(Library, on_delete=models.CASCADE, null=True, related_name='members')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['member_id'], name='unique_member_id'
            )
        ]

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    book_id = models.CharField(max_length=100, default=None)
    title = models.CharField(max_length=100, default = None)
    author = models.CharField(max_length=100, default = None)
    owned_by = models.ForeignKey(Library, on_delete=models.CASCADE, null=True, related_name='books')
    is_borrowed = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    borrowed_by = models.ForeignKey(Member, on_delete=models.DO_NOTHING, null=True, default=None)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book_id'], name='unique_book_id'
            )
        ]

    def borrow(self, member: Member):
        self.borrowed_by = member
        self.is_borrowed = True
        self.save()
    
    def giveBack(self):
        self.borrowed_by = None
        self.is_borrowed = False
        self.save()

    def __str__(self):
        return f"{self.book_id}, {self.title}, {self.author}, {self.is_borrowed}"