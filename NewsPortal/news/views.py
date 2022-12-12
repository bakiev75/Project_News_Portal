from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
# from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm, ArticleForm
from .models import Post
from .filters import NewsFilter

class NewsList(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time_post'  # Поле, которое будет использоваться для сортировки объектов - дата
    template_name = 'news.html'  # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка новостей
    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # Анонс горячих новостей.
        context['hot_news'] = None
        return context


class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — new.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранная пользователем новость
    context_object_name = 'new'


class SearchNewsList(ListView):  # Создаю новый класс для страницы поиска /news/search
    model = Post  # Указываем модель, объекты которой мы будем выводить
    # ordering = '-date_time_post'            # Поле, которое будет использоваться для сортировки объектов - дата
    ordering = '-date_time_post'  # Поле, которое будет использоваться для сортировки объектов - дата
    template_name = 'search.html'  # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


# Добавляем новое представление для создания новости.
class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_new = 'NEW'
        return super().form_valid(form)


# Добавляем представление для изменения новости.
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


# Представление удаляющее новость.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


# Добавляем новое представление для создания статьи.
class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # модель
    model = Post

    # и новый шаблон, в котором используется форма.
    template_name = 'articles_create.html'

    send_mail(
        subject=Post.title,
        message='Test',
        from_email='andrey.bakiev75@yandex.ru',
        recipient_list=['andrey.bakiev@gmail.com']
    )

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_new = 'ART'
        return super().form_valid(form)


    # send_mail(
    #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
    #     # имя клиента и дата записи будут в теме для удобства
    #     message=appointment.message,  # сообщение с кратким описанием проблемы
    #     from_email='peterbadson@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
    #     recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
    # )


# Добавляем представление для изменения статьи.
class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = NewsForm
    model = Post
    template_name = 'articles_edit.html'


# Представление удаляющее статью.
class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles_list')
# Create your views here.
