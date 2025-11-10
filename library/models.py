from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    @property
    def available_copies_count(self):
        # Counts total copies minus active loans
        return self.total_copies - self.loan_set.count()

    @property
    def is_available(self):
        return self.available_copies_count > 0

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loan_set')
    patron = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.book.title} loaned to {self.patron.username}"

class BookMessage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='messages')
    patron = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.patron.username} on {self.book.title}"