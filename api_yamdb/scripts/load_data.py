import csv

from django.conf import settings
from reviews.models import Comment, Review
from title.models import Category, Genre, GenreTitle, Title
from users.models import User


def run():
    with open(f'{settings.BASE_DIR}/static/data/users.csv') as file:
        reader = csv.reader(file)
        next(reader)
        User.objects.all().delete()
        for row in reader:
            _, user = User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6]
            )

    with open(f'{settings.BASE_DIR}/static/data/category.csv') as file:
        reader = csv.reader(file)
        next(reader)
        Category.objects.all().delete()
        for row in reader:
            _, category = Category.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )

    with open(f'{settings.BASE_DIR}/static/data/genre.csv') as file:
        reader = csv.reader(file)
        next(reader)
        Genre.objects.all().delete()
        for row in reader:
            _, comment = Genre.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )

    with open(f'{settings.BASE_DIR}/static/data/titles.csv') as file:
        reader = csv.reader(file)
        next(reader)
        Title.objects.all().delete()
        for row in reader:
            _, title = Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3])
            )

    with open(f'{settings.BASE_DIR}/static/data/review.csv') as file:
        reader = csv.reader(file)
        next(reader)
        Review.objects.all().delete()
        for row in reader:
            _, rewiew = Review.objects.get_or_create(
                id=row[0],
                title=Title.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5]
            )

    with open(f'{settings.BASE_DIR}/static/data/genre_title.csv') as file:
        reader = csv.reader(file)
        next(reader)
        GenreTitle.objects.all().delete()
        for row in reader:
            _, rewiew = GenreTitle.objects.get_or_create(
                id=row[0],
                title=Title.objects.get(id=row[1]),
                genre=Genre.objects.get(id=row[2])

            )

    with open(f'{settings.BASE_DIR}/static/data/comments.csv') as file:
        reader = csv.reader(file)
        next(reader)
        Comment.objects.all().delete()
        for row in reader:
            _, comment = Comment.objects.get_or_create(
                id=row[0],
                review=Review.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4]
            )


if __name__ == "__main__":
    run()
