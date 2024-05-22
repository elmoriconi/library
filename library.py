class Book:
    
    def __init__(self, book_id: str, title: str, author: str) -> None:
        self.book_id: str = book_id
        self.title: str = title
        self.author: str = author
        self.is_borrowed: bool = False
        
    def __str__(self):
        return f"{self.book_id}, {self.title}, {self.author}, {self.is_borrowed}"
        
    def borrow(self):
        if self.is_borrowed != True:
            self.is_borrowed = True
        
    def return_book(self):
        self.is_borrowed = False

class Member:
    
    def __init__(self, member_id: str, name: str) -> None:
        self.member_id: str = member_id
        self.name: str = name
        self.borrowed_books: list[Book] = []
        
    def __str__(self):
        return f"{self.member_id}, {self.name}, {self.borrowed_books}"
    
    def borrow_book(self, book: Book):
        if book.is_borrowed == False:
            self.borrowed_books.append(book)
    
    def return_book(self, book):
        self.borrowed_books.remove(book)

class Library:
    
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        
    def add_book(self, book_id: str, title: str, author: str):
        book = Book(book_id, title, author)
        self.books.update({book_id: book})
        
    def register_member(self, member_id: str, name: str):
        member = Member(member_id, name)
        self.members.update({member_id: member})
        
    def borrow_book(self, member_id: str, book_id: str):
        if member_id in self.members:
            member = self.members.get(member_id)
        else: 
            raise ValueError("Member not found")
        if book_id in self.books:
            book = self.books.get(book_id)
        else:
            raise ValueError("Book not found")
        if book.is_borrowed == False:
            member.borrowed_books.append(book.title)
            book.is_borrowed = book.borrow()
        else:
            raise ValueError("Book is already borrowed")
    
    def return_book(self, member_id: str, book_id: str):
        member = self.members.get(member_id)
        book = self.books.get(book_id)
        if book.title in member.borrowed_books:
            member.borrowed_books.remove(book.title)
            book.is_borrowed = False
        else:
            raise ValueError("Book not borrowed by this member")
            
    def get_borrowed_books(self, member_id):
        if member_id in self.members:
            member = self.members.get(member_id)
            return member.borrowed_books
        else:
            raise ValueError("Member not found")