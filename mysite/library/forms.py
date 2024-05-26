from django import forms
from .models import Book, Member

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_id', 'name']
