# Generated by Django 5.2.3 on 2025-07-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_article_function_alter_article_shortcut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='article.image'),
        ),
    ]
