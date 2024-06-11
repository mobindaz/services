from django.urls import path
from . import views as students

app_name = 'students'
urlpatterns = [
	path('allstudents',students.AllStudents.as_view(),name='allstudents'),
	path('students',students.StudentsPendingVerification.as_view(),name='students'),
	path('verifiedstudents',students.VerifiedStudentView.as_view(),name='verifiedstudents'),
	path('student/<int:pk>',students.StudentDetailView.as_view(),name='student'),
	path('students/<int:pk>/edit',students.StudentEditView.as_view(),name='edit_student')
]