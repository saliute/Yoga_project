import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from tinymce.models import HTMLField



class Type(models.Model):
    name = models.CharField('Title', max_length=200, help_text='Entry lesson title')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"


class Lesson(models.Model):
    title = models.CharField('Title', max_length=200)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, related_name='lessons')
    summary = models.TextField('Description', max_length=1000, help_text='Short lesson description')
    type = models.ManyToManyField('Type', help_text='Please choose type of this lesson')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)
    price = models.IntegerField('Price', null=True)

    def display_type(self):
        return '; '.join([type.name for type in self.type.all()])

    display_type.short_description = 'Type'

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('lesson-detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class LessonInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique lesson code')
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField('Will be available', null=True, blank=True)

    LOAN_STATUS = (
        ('p', 'Planning'),
        ('a', 'Not available'),
        ('b', 'You can book'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Status'
    )

    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']  # admin svetainės settingas, kaip rikiuojama

    def __str__(self):
        return f'{self.id} {self.lesson.title}'


class Teacher(models.Model):
    first_name = models.CharField('Name', max_length=100)
    last_name = models.CharField('Surname', max_length=100)
    description = HTMLField(default="cia turi buti pamokos aprasymas")

    def display_lessons(self):
        return ', '.join([lesson.title for lesson in self.lessons.all()][:3]) + "..."

    display_lessons.short_description = 'Lessons'

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('teacher-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Blog(models.Model):
    title = models.CharField('Title', max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Description', max_length=1000, help_text='Short description')
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField('Title', max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField('Viršelis', upload_to='covers', null=True)

    def __str__(self):
        return self.title
