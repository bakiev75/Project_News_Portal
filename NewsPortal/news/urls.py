from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewDetail, SearchNewsList, NewsCreate, NewsUpdate, NewsDelete

from .views import CategoryListViev, subscribe

from django.views.decorators.cache import cache_page

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60*10)(NewsList.as_view()), name='news_list'),               # Кэш
   path('<int:pk>', NewDetail.as_view(), name='post_detail'),
   path('search/', SearchNewsList.as_view()),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryListViev.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
# Для проверки таски делаем отдельную страницу
   # path('tasks/', TasksView.as_view()),
]
