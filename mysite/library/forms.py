from django import forms
from .models import Book, Member, Library

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_id', 'name']

class LibraryForm(forms.ModelForm):
    class Meta:
        model: Library
        fields = ['books', 'members', 'name']