from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import datetime

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    patron = models.ForeignKey(User, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = datetime.date.today() + timedelta(days=14)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} loaned to {self.patron.username}"