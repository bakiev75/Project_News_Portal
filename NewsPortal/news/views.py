from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post                            # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time_post'            # Поле, которое будет использоваться для сортировки объектов - дата
    template_name = 'news.html'             # Указываем имя шаблона, в котором будут все инструкции о том,
                                            # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'            # Это имя списка, в котором будут лежать все объекты.
                                            # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.

class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранная пользователем новость
    context_object_name = 'new'


# Create your views here.
