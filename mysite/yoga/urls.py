from django.urls import path, include
from unicodedata import name

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/<int:teacher_id>', views.teacher, name='teacher-detail'),
    path('lessons/', views.LessonListView.as_view(), name='lessons'),
    path('lessons/<int:pk>', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mylessons/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed')

]
