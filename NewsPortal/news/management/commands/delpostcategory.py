from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category, PostCategory


class Command(BaseCommand):
    help = 'Удаляет все новости и статьи из одной выбранной категории.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: ')

        # if answer != 'yes':
        #     self.stdout.write(self.style.ERROR('Отказано в доступе.'))
        # else:
        #     if  Post.objects.filter(category__name__contains=options["category"]):
        #         Post.objects.filter(category__name__contains=options["category"]).delete()
        #         self.stdout.write(self.style.SUCCESS(f'Удалены все статьи и новости в категории {options["category"]}'))
        #     else:
        #         self.stdout.write(self.style.ERROR(f'Не найдены записи в категории {options["category"]}'))

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отказано в доступе.'))
            return

        try:
            print('Начало try')
            category_1 = Category.objects.get(name=options["category"])
            print(category_1)                                               # Проверка имени объекта класса
            Post.objects.filter(category == category_1).delete()
            self.stdout.write(self.style.SUCCESS(f'Удалены все статьи и новости в категории {options["category"]}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не найдены записи в категории {options["category"]}'))
