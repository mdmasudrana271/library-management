from django.db import models
from usersapp.models import UserAccount
from booksapp.models import Book


from .constants import TRANSACTION_TYPE

# Create your models here.



class Transaction(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
