from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Course, Enrollment, Submission, Learner


def registration_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Learner.objects.create(user=user, occupation='student')
            login(request, user)
            return HttpResponseRedirect(reverse('onlinecourse:course_list'))
    else:
        form = UserCreationForm()
    return render(request, 'onlinecourse/user_registration_bootstrap.html', {'form': form})


class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.annotate(
            total_enrollment=Count('enrollment')
        ).order_by('-total_enrollment')[:10]


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        enrolled = False

        if self.request.user.is_authenticated:
            enrolled = Enrollment.objects.filter(
                learner__user=self.request.user,
                course=course
            ).exists()

        context['course'] = course
        context['enrolled'] = enrolled
        return context


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    learner = get_object_or_404(Learner, user=request.user)

    Enrollment.objects.get_or_create(
        learner=learner,
        course=course
    )

    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    learner = get_object_or_404(Learner, user=request.user)
    enrollment = get_object_or_404(Enrollment, learner=learner, course=course)

    if request.method == 'POST':
        selected_choices = []

        for key in request.POST:
            if key.startswith('choice'):
                values = request.POST.getlist(key)
                for value in values:
                    selected_choices.append(int(value))

        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(selected_choices)

        return HttpResponseRedirect(
            reverse('onlinecourse:show_exam_result', args=(course.id, submission.id))
        )

    return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    questions = course.question_set.all()

    total_score = 0
    gained_score = 0
    selected_choice_ids = submission.choices.values_list('id', flat=True)

    for question in questions:
        total_score += question.grade
        if question.is_get_score(selected_choice_ids):
            gained_score += question.grade

    if total_score > 0:
        grade = int((gained_score / total_score) * 100)
    else:
        grade = 0

    context = {
        'course': course,
        'submission': submission,
        'grade': grade,
        'score': gained_score,
        'total': total_score,
        'questions': questions,
        'selected_choice_ids': selected_choice_ids,
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)