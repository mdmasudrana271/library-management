# from django.contrib import admin
# from . models import Category
# # Register your models here.
# admin.site.register(Category)


from django.contrib import admin

from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ['name', 'slug']
    
admin.site.register(models.Category, CategoryAdmin)