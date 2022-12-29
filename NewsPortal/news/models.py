from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# - связь "один к одному" с встроенной моделью пользователей User;
# - рейтинг пользователя (FloatField).
# Метод upgrade_rating(), который обновляет рейтинг пользователя, переданный в аргумент этого метода:
#   Метод состоит из следующего:
#   - суммарный рейтинг каждой статьи автора умножается на 3;
#   - суммарный рейтинг всех комментариев АВТОРА;
#   - суммарный рейтинг всех комментариев к статьям автора.


class Author(models.Model):                                                         # Модель 1
    rating_author = models.FloatField(default=0.0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)                   # Поле связи "один к одному" с встроенной
                                                                                    # моделью пользователей User;
    def __str__(self):
        return f'{self.author}'

    def update_rating(self):                                                        # Метод upgrade_rating()
        rating_post = self.post_set.all().aggregate(s1=Sum('rating_article_or_new'))['s1']
        rating_comment = Comment.objects.filter(user_comment__author=self).aggregate(s2=Sum('rating_comment'))['s2']
        rating_comment_post = Comment.objects.exclude(user_comment__author=self).aggregate(s3=Sum('rating_comment'))['s3']
        self.rating_author = rating_post * 3 + rating_comment + rating_comment_post
        self.save()


# Модель Category
# Категории новостей/статей - темы, которые они отражают (спорт, политика, образование и т.д.)
# Имеет единственное поле: название категории. Поле должно быть уникальным
# (в определении поля необходимо написать параметр unique = True)


class Category(models.Model):                                                       # Модель 2
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name

# Модель Post
# Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну, или несколько категорий.
# Модель должна включать поля:
# - поле с выбором - "статья" или "новость"
# - заголовок "статьи" или "новости"
# - текст "статьи" или "новости"
# - автоматически добавляемая дата и время создания
# - рейтинг "статьи" или "новости"
# - связь "один ко многим" с моделью Author
# - связь "многие ко многим" с моделью Category (с дополнительной моделью PostCategory)
#
# Методы
# - like() увеличивает рейтинг на единицу
# - dislike() уменьшает рейтинг на единицу
# - preview() возвращает начало статьи длиной 124 символа и добавляет многоточие в конце


article = 'ART'
new = 'NEW'

POSITIONS = [
    (article, 'Статья'),
    (new, 'Новость'),
]


class Post(models.Model):                                                                   # Модель 3
    author = models.ForeignKey(Author, on_delete=models.CASCADE)                            # - связь "один ко многим" с моделью Author
    article_or_new = models.CharField(max_length=3, choices=POSITIONS, default=article)     # ART - статья; NEW - новость
    title = models.CharField(max_length=255)                                                # Заголовок статьи или новости
    text_body = models.TextField(default='No text')                                         # Текст статьи или новости
    date_time_post = models.DateTimeField(auto_now_add=True)                                # Дата и время СОЗДАНИЯ записи
    rating_article_or_new = models.FloatField(default=0.0)                                  # Рейтинг статьи или новости
    category = models.ManyToManyField(Category, through='PostCategory')                     # - связь "многие ко многим" с моделью Category (через модель PostCategory)

                                                                            #   Методы
    def like_post(self):                                                    # - like_post() увеличивает рейтинг на единицу
        self.rating_article_or_new += 1
        self.save()

    def dislike_post(self):                                                 # - dislike_post() уменьшает рейтинг на единицу
        self.rating_article_or_new -= 1
        self.save()

    def preview_post(self):                                                 # - preview() возвращает начало статьи длиной
        return str(self.text_body)[:20] + '...'                            # 124 символа и добавляет многоточие в конце

    def title_as_text(self):
        return str(self.title)

    def __str__(self):
        return f'{self.title} {self.text_body[:20]}' + '...'


    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):                                           # Модель 4
    post = models.ForeignKey(Post, on_delete=models.CASCADE)                # - связь "один ко многим" с моделью Post
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category

# Модель Comment
# Под каждой статьёй/новостью можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# - текст комментария
# - дата и время СОЗДАНИЯ комментария
# - рейтинг комментария
# - связь "один ко многим" с моделью Post
# - связь "один ко многим" со встроенной моделью User (комментарии может оставить любой пользователь, не только Author)
#
#   Методы
# - like() увеличивает рейтинг на единицу
# - dislike() уменьшает рейтинг на единицу


class Comment(models.Model):                                                # Модель 5
    text_comment = models.TextField(default='No comment')                   # Текст комментария
    date_time_comment = models.DateTimeField(auto_now_add=True)             # Дата и время СОЗДАНИЯ комментария
    rating_comment = models.FloatField(default=0.0)                         # Рейтинг комментария
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)      # Связь "один ко многим" с моделью Post
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)      # - связь "один ко многим" со встроенной
                                                                            #   моделью User (коммент/ может оставить любой User, не только Author)
                                                                            #   Методы
    def like_comment(self):                                                 # - like() увеличивает рейтинг на единицу
        self.rating_comment = self.rating_comment + 1
        self.save()

    def dislike_comment(self):                                              # - dislike() уменьшает рейтинг на единицу
        self.rating_comment = self.rating_comment - 1
        self.save()

    def __str__(self):
        return str(self.text_comment)[:124] + '...'

# Create your models here.
