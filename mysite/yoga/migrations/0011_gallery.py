# Generated by Django 4.1.1 on 2023-01-30 15:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('yoga', '0010_blog_title_alter_blog_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='Title')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('content',
                 models.CharField(help_text='Short photos description', max_length=1000, verbose_name='Description')),
                ('cover', models.ImageField(null=True, upload_to='covers', verbose_name='Viršelis')),
            ],
        ),
    ]
