from django.contrib import admin

from .models import Teacher, Type, Lesson, LessonInstance


class LessonsInstanceInline(admin.TabularInline):
    """knygų egzempliorių vaizdavimo klasė
    (sukuria eilutes kurias galima įdėti į kitą viewsą)"""
    model = LessonInstance  # modelis iš kurio kuriamos eilutės(turi būti vaikinis kitam modeliui)
    # readonly_fields = ('id',)  # nurodom kad id lauko šiam viewse negalima redaguoti
    # can_delete = False  # negalima trinti
    extra = 0  # kad nepridėtų į viewsą tuščių eilučių


# VISOS iš admin.ModelAdmin paveldinčios klasės keičia standartinį modelio viewsą admin svetainėje
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'display_type', 'get_teachname')  # nurodom kokius stulpelius vaizduosime BookInstance
    # viewse admin svetainėje
    # display_genre atsiranda iš metodo aprašyto Book modelyje,
    # models.py faile
    search_fields = ('teacher__last_name',)
    def get_teachname(self, obj): # BONUS - būdas per foreign key pasiekti konkretų lauką tėvinėj lentelėj
        return obj.teacher.first_name
    get_teachname.short_description = 'Teacher name'
    inlines = [LessonsInstanceInline]  # prijungiam papildomą vaizdą(eilutes) iš class BooksInstanceInline


class LessonInstanceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'status', 'due_back', 'student')  # stulpeliai BookInstance viewse admin svetainėje
    list_filter = ('status', 'due_back')  # sukuriamas filtro skydelis
    search_fields = ('id', 'lesson__title')  # paieškos laukas
    list_editable = ('due_back', 'status', 'student')  # nurodom kad į list_display įtraukti stulpeliai gali būti redaguojami

    fieldsets = (  # sukuria atskirus tabus laukams (šie laukai rodomi defaultu, čia sukuriamas tik padalinimas)
        ('General', {'fields': ('id', 'lesson',)}),  # General, Availability - mūsų sukurti tabų pavadinimai, žodynuose
        ('Availability', {'fields': ('status', 'due_back', 'student')})  # raktuose fields nurodoma kokie laukai bus kokiam tabe
    )


class TeacherAdmin(admin.ModelAdmin):  # stulpeliai Author viewse admin svetainėje
    list_display = ('last_name', 'first_name', 'display_lessons')


# !!! kad nūtų naudojami mūsų sukurti admin viewsai, viewsų klases reikia surišti su modelių klasėmis
# panaudojus admin.site.register metodą
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Type)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonInstance, LessonInstanceAdmin)
