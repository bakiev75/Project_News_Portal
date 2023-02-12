from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет все новости и статьи из одной выбранной категории.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument("category1", type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category1"]}? yes/no: ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отказано в доступе.'))
        else:
            try:
                category = Category(name=options["category1"])
                posts = Post.objects.filter(article_or_new == 'NEW')
                print(posts)
                self.stdout.write(self.style.SUCCESS(f'Выполнено удаление всех записей в категории {category}'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Не найдены записи в категории {options["category1"]}'))
