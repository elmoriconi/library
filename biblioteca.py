class Book:
    def __init__(self, book_id: str, title: str, author: str, is_borrowed: bool) -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        
    def borrow(self):
        if self.is_borrowed:
            return 0
        else:
            self.is_borrowed = True
    
    def get(self):
        return self.is_borrowed
            
    def return_book(self):
        self.is_borrowed = False
    
    def __str__(self):
        return f"{self.title}"

class Member:
    def __init__(self, member_id: str, name: str) -> None:
        self.member_id = member_id
        self.name = name
        self.borrowed_books: list[Book] = []
    
    def borrow_book(self, book: Book):
        if book.get():
            raise ValueError("Book is already borrowed")
        else:
            self.borrowed_books.append(book)
            book.borrow()
            
    def return_book(self, book: Book):
        if book not in self.borrowed_books:
            raise ValueError("Book not borrowed by this member")
        book.return_book()
        self.borrowed_books.remove(book)
        
        
class Library:
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.member: dict[str, Member] = {}
    
    def add_book(self, book_id: str, title: str, author: str):
        self.books[book_id] = Book(book_id, title, author, False)
    
    def register_member(self, member_id: str, name: str):
        self.member[member_id] = Member(member_id, name)
        
    def borrow_book(self, member_id: str, book_id: str):
        if book_id not in self.books:
            raise ValueError("Book not found")
        if member_id not in self.member:
            raise ValueError("Member not found")
        self.member[member_id].borrow_book(self.books[book_id])
        
    def return_book(self, member_id: str, book_id: str):
        self.member[member_id].return_book(self.books[book_id])
        
    def get_borrowed_books(self, member_id: str):
        lista: list[Book] = []
        for i in range(len(self.member[member_id].borrowed_books)):
            if self.member[member_id].borrowed_books[i].is_borrowed:
                lista.append(self.member[member_id].borrowed_books[i].title)
        return lista