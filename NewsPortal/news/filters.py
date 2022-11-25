import django_filters
from django_filters import FilterSet, CharFilter, DateFromToRangeFilter, NumberFilter
from django_filters.widgets import RangeWidget

from .models import Post

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.

class NewsFilter(FilterSet):
    author__author__username = CharFilter(lookup_expr = 'icontains')
    # date_time_post = NumberFilter(field_name='date_time_post', lookup_expr='gt')
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           'title': ['icontains'],
           'date_time_post':['gt']
       }

# class NewsFilter(FilterSet):
#     author__author__username = CharFilter(lookup_expr = 'icontains')
#     date_range = DateFromToRangeFilter(widget=RangeWidget({{<input type="date">}})
#     class Meta:
#        # В Meta классе мы должны указать Django модель,
#        # в которой будем фильтровать записи.
#        model = Post
#        # В fields мы описываем по каким полям модели
#        # будет производиться фильтрация.
#        fields = {
#            'title': ['icontains'],
#        }