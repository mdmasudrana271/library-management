from django.views.generic import DetailView,CreateView
from . import forms
from . import models
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from borrowingapp.models import Borrow
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class DetailBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'
    
    # def post(self, request, *args, **kwargs):
    #     reviews_form = forms.ReviewsForm(data=self.request.POST)
    #     book = self.get_object()
    #     if reviews_form.is_valid():
    #         new_review = reviews_form.save(commit=False)
    #         new_review.book = book
    #         new_review.save()
    #     return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object 
        reviews = book.reviews.all()
        # reviews_form = forms.ReviewsForm()
        if self.request.user.is_authenticated:
            user = self.request.user.account
            has_borrowed = Borrow.objects.filter(book=book,user=user, status='Borrowed').exists()
        else:
            has_borrowed = False
        
        context['has_borrowed'] = has_borrowed
        context['reviews'] = reviews
        # context['reviews_form'] = reviews_form
        return context
    
@method_decorator(login_required, name='dispatch')
class AddReview(CreateView):
    model = models.Reviews
    form_class = forms.ReviewsForm
    template_name = 'add_review.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews_form = forms.ReviewsForm()
        context['reviews_form'] = reviews_form
        return context


    def form_valid(self,form):
        book = get_object_or_404(models.Book, id=self.kwargs['id'])
        form.instance.book = book
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('detail_book', kwargs={'id': self.kwargs['id']})

    
    