from django.db import models
from categoryapp.models import Category

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads')
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class Reviews(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comments by {self.name}"