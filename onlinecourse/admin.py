from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ['name', 'pub_date']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_time', 'total_learners']

@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['enrollment']