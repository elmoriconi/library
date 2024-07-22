from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100, default = None, unique = True, primary_key=True)

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