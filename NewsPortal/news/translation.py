from .models import Category, Post                                      # импортируем декоратор для перевода и класс
from modeltranslation.translator import register, TranslationOptions    # настроек, от которого будем наследоваться


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
   fields = ('name',)                                  # указываем, какие именно поля надо переводить в виде кортежа



@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text_body', )
