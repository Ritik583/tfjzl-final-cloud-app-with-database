from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('submit/<int:course_id>/', views.submit, name='submit'),
    path(
        'course/<int:course_id>/submission/<int:submission_id>/',
        views.show_exam_result,
        name='show_exam_result'
    ),
    path('registration/', views.registration_request, name='registration'),

    # ✅ ADD THESE
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]