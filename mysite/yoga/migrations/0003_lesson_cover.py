# Generated by Django 4.1.1 on 2023-01-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yoga', '0002_alter_lesson_options_alter_types_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='cover',
            field=models.ImageField(null=True, upload_to='covers', verbose_name='Virselis'),
        ),
    ]