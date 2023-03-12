from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
# from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.core.mail import EmailMultiAlternatives     # импортируем класс для создания объекта письма с html
from django.template.loader import render_to_string     # импортируем функцию, которая срендерит наш html в текст

from .forms import NewsForm, ArticleForm
from .models import Post, Category
from .filters import NewsFilter

from django.utils.translation import gettext as _

# from .tasks import hello, printer
from django.http import HttpResponse

from django.utils import timezone
from django.shortcuts import redirect, render

import pytz                                     #  импортируем стандартный модуль для работы с часовыми поясами


class Index(View):
    def get(self, request):
        string = _('Hello, world!')
        # return HttpResponse(string)

        context = {
            'string': string
        }
        return HttpResponse(render(request, 'index.html', context))

class NewsList(ListView):
    curent_time = timezone.now()
    model = Post                    # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time_post'    # Поле, которое будет использоваться для сортировки объектов - дата
    template_name = 'news.html'     # Указываем имя шаблона, в котором будут все инструкции о том,
                                    # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'    # Это имя списка, в котором будут лежать все объекты.
                                    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10                # вот так мы можем указать количество записей на странице

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
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # Анонс горячих новостей.
        context['hot_news'] = None
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')

class CategoryListViev(NewsList):                           # Создание в процессе вебинара
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_time_post')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписаны на рассылку новостей категории '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


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

        # html_content = render_to_string(                                # получаем наш html
        #     'for_post_create.html',
        #     {
        #         'post': post,
        #     }
        # )

        # в конструкторе уже знакомые нам параметры. Называются правда немного по-другому, но суть та же.
        # msg = EmailMultiAlternatives(
        #     subject=f'{post.title}',
        #     body=post.text_body,                                        # это то же, что и message
        #     from_email='andrey.bakiev75@yandex.ru',
        #     to=['andrey.bakiev@gmail.com'],                             # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        #
        # msg.send()  # отсылаем


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


    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_new = 'ART'

        # send_mail(                                              # Отправка на почту из списка
        #     subject=post.title,
        #     message=post.text_body,
        #     from_email='andrey.bakiev75@yandex.ru',
        #     recipient_list=['andrey.bakiev@gmail.com']          # Заменить на почту по подписке
        # )

        return super().form_valid(form)


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

# Представление для проверки работы таски, при вызове страницы по адресу news/tasks/

# class TasksView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta = datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')
