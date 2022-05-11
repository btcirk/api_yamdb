from django.core.management.base import BaseCommand
from csv import DictReader
from reviews.models import Genre, Comment, Category, Title, Review
from django.contrib.auth import get_user_model

User = get_user_model()

ALREDY_LOADED_ERROR_MESSAGE = 'База не пустая, загрузка отменена'

model_file_csv = [
    # {'model': User, 'path': 'users.csv'},
    {'model': Category, 'path': 'category.csv'},
    # {'model': Comment, 'path': 'comments.csv'},
    {'model': Genre, 'path': 'genre.csv'},
    # {'model': Genre, 'path': 'genre_title.csv'},
    # {'model': Review, 'path': 'review.csv'},
    # {'model': Title, 'path': 'titles.csv'},
]


class Command(BaseCommand):

    help = "Загрузка данных из .csv"

    def handle(self, *args, **options):

        for row in DictReader(open('./static/data/users.csv',
                              encoding="utf-8-sig")):
            model_save = User(id=row['id'], username=row['username'],
                              email=row['email'])
            model_save.save()

        for file_csv in model_file_csv:
            model = file_csv['model']
            path = file_csv['path']

            if model.objects.exists():
                print(f'Модель {model.__name__} '
                      f'ошибка: {ALREDY_LOADED_ERROR_MESSAGE}')
                continue

            print(f'Загрузка модели {model.__name__}')

            for row in DictReader(open(f'./static/data/{path}',
                                  encoding="utf-8-sig")):

                model_save = model(**row)
                model_save.save()

        for row in DictReader(open('./static/data/titles.csv',
                              encoding="utf-8-sig")):

            model_save = Title(id=row['id'], name=row['name'],
                               year=row['year'], category_id=row['category'],)
            model_save.save()

        for row in DictReader(open('./static/data/review.csv',
                              encoding="utf-8-sig")):

            model_save = Review(id=row['id'], title_id=row['title_id'],
                                text=row['text'], author_id=row['author'],
                                pub_date=row['pub_date'], score=row['score'])
            model_save.save()

        for row in DictReader(open('./static/data/comments.csv',
                              encoding="utf-8-sig")):

            model_save = Comment(id=row['id'], review_id=row['review_id'],
                                 text=row['text'], author_id=row['author'],
                                 pub_date=row['pub_date'])
            model_save.save()

        for row in DictReader(open('./static/data/genre_title.csv',
                              encoding="utf-8-sig")):

            obj = Title.objects.get(pk=row['title_id'])
            obj.genre.add(Genre.objects.get(pk=row['genre_id']))
            obj.save()
