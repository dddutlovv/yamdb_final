from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User
from title.models import Title


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True, db_index=True
    )

    class Meta:
        unique_together = ('author', 'title')
        ordering = ['id']

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'pub_date',
        auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text
