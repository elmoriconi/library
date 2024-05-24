from django.db import models

class Book(models.Model):
    
    def __init__(self, book_id: str, title: str, author: str) -> None:
        self.book_id: str = book_id
        self.title: str = title
        self.author: str = author
        self.is_borrowed: bool = False
        
    def __str__(self):
        return f"{self.book_id}, {self.title}, {self.author}, {self.is_borrowed}"
        
    def borrow(self):                       #if book not borrowed, turns is_borrowed to True
        if not self.is_borrowed:
            self.is_borrowed = True
        
    def return_book(self):                  #if book borrowed, turns is borrowed to False<
        if self.is_borrowed:
            self.is_borrowed = False

class Member(models.Model):
    
    def __init__(self, member_id: str, name: str) -> None:
        self.member_id: str = member_id
        self.name: str = name
        self.borrowed_books: list[Book] = []
        
    def __str__(self):
        return f"{self.member_id}, {self.name}, {self.borrowed_books}"
    
    def borrow_book(self, book: Book):
        if book.is_borrowed:                 #if book already borrowed, raise error
            raise ValueError("Book is already borrowed")
        else:                                #else append book to member's list, then turns book.is_borrowed to True
            self.borrowed_books.append(book)
            book.borrow()
    
    def return_book(self, book: Book):
        if book not in self.borrowed_books:  #if member's list doesn't contain book, raise error
            raise ValueError("Book not borrowed by this member")
        book.return_book()                   #else turns book.is_borrowed to False and removes it from member's list
        self.borrowed_books.remove(book)

class Library(models.Model):
    
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        
    def add_book(self, book_id: str, title: str, author: str):  
        self.books[book_id] = Book(book_id, title, author)
        
    def register_member(self, member_id: str, name: str):
        self.members[member_id] = Member(member_id, name)
        
    def borrow_book(self, member_id: str, book_id: str):
        if book_id not in self.books:         #if book not in books dictionary, raise error
            raise ValueError("Book not found")
        if member_id not in self.members:     #if member not in members dictionary, raise error
            raise ValueError("Member not found")
        self.members[member_id].borrow_book(self.books[book_id])   #by calling function borrow_book, adds book to member's list and turns is_borrowed to True
    
    def return_book(self, member_id: str, book_id: str):
        if book_id not in self.books:         #if book not in books dictionary, raise error
            raise ValueError("Book not found")
        if member_id not in self.members:     #if member not in members dictionary, raise error
            raise ValueError("Member not found")
        self.members[member_id].return_book(self.books[book_id])    #by calling function return_book, removes book from member's list and turns is_borrowed to False
            
    def get_borrowed_books(self, member_id):
        if member_id in self.members:
            member = self.members.get(member_id)    #gets member's info to access it's borrowed_books
            return member.borrowed_books
        else:
            raise ValueError("Member not found")    #if member not in members dictionary, raise error