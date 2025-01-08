from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('borrowig/<int:book_id>/', views.BorrowBookView.as_view(), name='borrow_book'),
    # path('borrowing/returning/<int:book_id>/', views.ReturnBookView.as_view(), name='return_book'),
    path('returning/<int:book_id>/', views.ReturnBookView.as_view(), name='return_book'),

]