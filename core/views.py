from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from booksapp.models import Book
from categoryapp.models import Category

# Create your views here.

class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'data'

    def get_queryset(self):
        queryset = Book.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        return context