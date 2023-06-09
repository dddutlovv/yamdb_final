# Generated by Django 3.2 on 2023-02-23 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('title', '0002_auto_20230223_0624'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='title.genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='title.title')),
            ],
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='title.GenreTitle', to='title.Genre', verbose_name='жанр'),
        ),
    ]
