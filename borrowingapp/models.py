from django.db import models
from usersapp.models import UserAccount
from booksapp.models import Book

# Create your models here.
class Borrow(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Borrowed', 'Borrowed'), ('Returned', 'Returned')],
        default='Borrowed',
    )

    def __str__(self):
        return f"{self.user.user.username} - {self.book.title} ({self.status})"