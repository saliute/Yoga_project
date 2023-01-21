from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Teacher, Lesson, LessonInstance


def index(request):
    # count užklausos(queries)
    num_lessons = Lesson.objects.all().count()  # suskaičiuojam knygas
    num_instances = LessonInstance.objects.all().count()  # suskaičiuojam knygų kopijas

    # suskaičiuojam laisvas knygas(statusas g)
    num_instances_available = LessonInstance.objects.filter(status__exact="g").count()

    # suskaičiuojam autorius
    num_teachers = Teacher.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1



    context = {  # šablono konteksto kintamasis
        'num_lessons': num_lessons,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_teachers': num_teachers,
        'num_visits': num_visits
    }

    # formuojam galutinį vaizdą iš šablono index.html ir duomenų
    # context žodyne(request - užklausa atėjusi iš kliento)
    return render(request, 'index.html', context=context)


def teachers(request):
    # authors = Author.objects.all()
    paginator = Paginator(Teacher.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_teachers = paginator.get_page(page_number)
    context = {
        'teachers': paged_teachers
    }
    return render(request, 'teachers.html', context=context)


def teacher(request, teacher_id):
    single_teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'teacher.html', {'teacher': single_teacher})


class LessonListView(generic.ListView):
    model = Lesson  # pagal modelio pav. autosukuriamas book_list kintamasis(visi objektai iš klasės) perduodamas į šabloną
    paginate_by = 4
    template_name = 'lesson_list.html'
    # context_object_name = 'my_book_list' galime pasikeisti automatinį konteksto kintamąjį(book_list) į custom pavadinimą


class LessonDetailView(generic.DetailView):
    model = Lesson  # šablonui autosukuriamas kintamas book
    template_name = 'lesson_detail_styled.html'


def search(request):
    query = request.GET.get("query")
    search_results = Lesson.objects.filter(
        Q(title__icontains=query) |
        Q(summary__icontains=query)
    )

    return render(request, "search.html", {"lessons": search_results, "query": query})

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = LessonInstance
    template_name = "user_lessons.html"


    def get_queryset(self):
        return LessonInstance.objects.filter(reader=self.request.user).filter(status__exact='p').order_by("due_back")

