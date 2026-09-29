from django.contrib import admin
# Seven imported classes from models.py: Course, Lesson, Instructor, Question, Choice, Submission, Enrollment
from .models import Course, Lesson, Instructor, Question, Choice, Submission, Enrollment


# QuestionInline class to allow adding/editing Questions directly in Course/Lesson views
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


# ChoiceInline class to allow adding/editing Choices inline within Question view
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


# QuestionAdmin class using ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'grade')


# LessonAdmin class using QuestionInline
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']
    inlines = [QuestionInline]


# CourseAdmin class using LessonInline
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Register models with their respective custom Admin classes
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)
