from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('allstudents/', views.AllStudents.as_view(), name='allstudents'),
    path('students/', views.StudentsPendingVerification.as_view(), name='students_pending_verification'),
    path('verifiedstudents/', views.VerifiedStudentView.as_view(), name='verified_students'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student'),
    path('students/<int:pk>/edit/', views.StudentEditView.as_view(), name='edit_student'),
    path('students_page/', views.AllStudents.as_view(), name='students_page'),
    path('save_imported_students/', views.save_imported_students, name='save_imported_students'),
    path('import_students/', views.ImportStudentsView.as_view(), name='import_students'),
    path('list_uploaded_files/', views.list_uploaded_files, name='list_uploaded_files'),
]
