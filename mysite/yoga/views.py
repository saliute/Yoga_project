from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Teacher, Lesson, LessonInstance, Blog, Gallery


def index(request):
    # count užklausos(queries)
    num_lessons = Lesson.objects.all().count()  # suskaičiuojam knygas
    num_instances = LessonInstance.objects.all().count()  # suskaičiuojam knygų kopijas

    # suskaičiuojam laisvas knygas(statusas g)
    num_instances_available = LessonInstance.objects.filter(status__exact="p").count()

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
    paginate_by = 3
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


class LoanedLessonsByUserListView(LoginRequiredMixin, generic.ListView):
    model = LessonInstance
    template_name = "user_lessons.html"

    def get_queryset(self):
        # return LessonInstance.objects.filter(student=self.request.user).filter(status__exact='p').order_by("due_back")
        return LessonInstance.objects.filter(student=self.request.user).order_by("due_back")


def blog(request):
    paginator = Paginator(Blog.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_blog = paginator.get_page(page_number)
    context = {
        'blog': paged_blog
    }
    return render(request, 'blog.html', context=context)


def gallery(request):
    paginator = Paginator(Gallery.objects.all(), 5)
    page_number = request.GET.get('page')
    paged_gallery = paginator.get_page(page_number)
    context = {
        'gallery': paged_gallery
    }
    return render(request, 'gallery.html', context=context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # Pasiimam reiksmes is registracijos formos lauku
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        # ar sutampa ivesti passwordai
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"User name {username} exist")
                return redirect("register")
            else:
                # ar nera tokio pacio emailo
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Emai {email} already exist")
                    return redirect("register")
                else:
                    # taskas kai viskas tvarkoje, patikrinimai praeiti, kuriam nauja useri
                    User.objects.create_user(username=username, email=email, password=password1)
                    messages.info(request, f"User {username} succsesfull registrated")
                    return redirect("login")
        else:
            messages.error(request, "Passwords not the same")
            return redirect("register")
    return render(request, "register.html")


@login_required(login_url='/yoga/accounts/login/', redirect_field_name='next')
def booklesson(request):
    # Logic for creating and saving a new book object
    # lessonID = request.POST["lessonID"]
    # print(lessonID)
    if request.method == "POST":
        lessonID = request.POST["lessonID"]
        print(lessonID)
        les = Lesson.objects.filter(id=lessonID)
        lesObj = Lesson.objects.get(id=lessonID)
        studentObj = User.objects.get(username=request.user)
        print(les)
        print(lesObj)
        print(request.user)
        messages.info(request, lessonID)
        lessonInst = LessonInstance(lesson = lesObj, student = studentObj)
        lessonInst.save()
        return render(request, "book_lesson.html")
    else:
        messages.error(request, "Book lesson againg")
        return redirect("")
