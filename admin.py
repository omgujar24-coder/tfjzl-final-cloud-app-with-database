from django.contrib import admin

# Imported all 7 required classes from .models
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
    Enrollment
)


# ChoiceInline allows adding choices directly within the Question admin page
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


# QuestionAdmin uses ChoiceInline to manage choices
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'grade')


# QuestionInline allows adding questions directly within the Lesson admin page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


# LessonAdmin uses QuestionInline to manage questions
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']
    inlines = [QuestionInline]


# LessonInline allows adding lessons directly within the Course admin page
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# CourseAdmin configures the Course model view
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Register all models with Django Admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Enrollment)
