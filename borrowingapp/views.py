from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from booksapp.models import Book
from .models import Borrow
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





def send_transaction_email(user, amount,book, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
            'book': book.title
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

@method_decorator(login_required, name='dispatch')
class BorrowBookView(View):
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        user = request.user.account  
        book = get_object_or_404(Book, id=book_id)
        existing_borrow = Borrow.objects.filter(book=book, status='Borrowed').exists()
        existing_return = Borrow.objects.filter(book=book, status='Returned').exists()
        if existing_borrow:
            messages.warning(request, "You have already borrowed this book.")
            return redirect('detail_book', id=book.id)
        if existing_return:
            user.balance -= book.borrowing_price
            user.save(update_fields=['balance']) 
            book.is_borrowed = True
            book.save(update_fields=['is_borrowed'])
            Borrow.objects.filter(user=user, book=book).update(status='Borrowed')
            Transaction.objects.create(
                account=user,
                book = book,
                amount = book.borrowing_price,
                balance_after_transaction=user.balance,
                transaction_type = 2,
            )
            messages.success(self.request,f'{"You have successfully borrowed this book. ${:,.2f}".format(float(book.borrowing_price))} was  deducted from your account.')
            send_transaction_email(self.request.user, book.borrowing_price,book, "Book Borrow Message", "borrow_book_email.html")
            return redirect('detail_book', id=book.id)
             
        if book.borrowing_price > user.balance:
            messages.warning(request, "Insufficient balance.")
            return redirect('detail_book', id=book.id)

        user.balance -= book.borrowing_price
        user.save(
            update_fields=[
                'balance'
            ]
        ) 
        book.is_borrowed = True
        book.save(
            update_fields=[
                'is_borrowed'
            ]
        )
        Borrow.objects.create(user=user, book=book, status='Borrowed')
        Transaction.objects.create(
                account=user,
                book = book,
                amount = book.borrowing_price,
                balance_after_transaction=user.balance,
                transaction_type = 2,
            ) 
        # messages.success(request, "You have successfully borrowed this book.")
        messages.success(self.request,f'{"You have successfully borrowed this book. ${:,.2f}".format(float(book.borrowing_price))} was  deducted from your account.')
        send_transaction_email(self.request.user, book.borrowing_price,book, "Book Borrow Message", "borrow_book_email.html")
        return redirect('detail_book', id=book.id)
    
@method_decorator(login_required, name='dispatch')
class ReturnBookView(View):
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')  

        borrow_record = Borrow.objects.get(id=book_id, status='Borrowed')
        # try:
        # except Borrow.DoesNotExist:
        #     messages.error(request, "Borrow record not found.")
        #     return redirect('home')  

        
        user = request.user.account
        book = borrow_record.book

        user.balance += book.borrowing_price
        user.save(update_fields=['balance'])

        book.is_borrowed = False
        book.save(update_fields=['is_borrowed'])

        borrow_record.status = "Returned"
        borrow_record.save(update_fields=['status'])
        Transaction.objects.create(
                account=user,
                book = book,
                amount = book.borrowing_price,
                balance_after_transaction=user.balance,
                transaction_type = 3,
            )

        # messages.success(request, "You have successfully returned this book.")
        messages.success(
            self.request,
            f'{"You have successfully returned this book.. ${:,.2f}".format(float(book.borrowing_price))} was returnend to your account.'
        )
        send_transaction_email(self.request.user, book.borrowing_price,book, "Book Return Message", "return_book_email.html")
        return redirect('detail_book', id=book.id)

