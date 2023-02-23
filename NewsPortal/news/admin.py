from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

# создаём новый класс для представления User в админке
class CategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['name'] # генерируем список имён всех полей для более красивого отображения

# создаём новый класс для представления User в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['author', 'title'] # генерируем список имён всех полей для более красивого отображения


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
# Register your models here.
