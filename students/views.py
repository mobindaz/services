from django.shortcuts import render, redirect
from django.views import View
from .models import Student, UploadedFile
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from .forms import StudentEditForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from tc.models import TcApplication
from django.contrib import messages
from io import TextIOWrapper
import csv

from .models import Student, UploadedFile

class ImportStudentsView(View):
    def get(self, request):
        return render(request, 'students/upload.html')

    def post(self, request):
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file:
            messages.error(request, 'No file uploaded.')
            return render(request, 'students/upload.html')
        
        # Save the uploaded file
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(csv_file.name, csv_file)
        file_url = fs.url(filename)
        
        # Save file information in the database
        UploadedFile.objects.create(file_name=csv_file.name, file_path=file_url)

        # Provide a success message
        messages.success(request, 'File successfully uploaded.')
        return render(request, 'students/upload.html')


def list_uploaded_files(request):
    files = UploadedFile.objects.all()
    return render(request, 'students/list_uploaded_files.html', {'files': files})


class AllStudents(View):
    template_name = 'students/students.html'
    def get(self, request, *args, **kwargs):
        context = {'label': 'Students'}
        headers = {
            'name': "Name",
            'admission_number': "Admission Number",
            'registration_number': "Registration Number",
            'department': "Department",
            'action': "Actions",
        }
        if 'a_number' in request.GET and request.GET['a_number']:
            searchkey = request.GET['a_number']
            students_objs = Student.objects.filter(Q(name__icontains=searchkey) | Q(admission_number__icontains=searchkey)).order_by('admission_number')
        else:
            students_objs = Student.objects.all().order_by('admission_number')
        
        paginator = Paginator(students_objs, 10)
        page = request.GET.get('page')
        students = paginator.get_page(page)
        context['headers'] = headers
        context['students'] = students
        return render(request, self.template_name, context)


class StudentsPendingVerification(View):
    template_name = 'students/students.html'
    def get(self, request, *args, **kwargs):
        context = {'label': 'Students'}
        headers = {
            'name': "Name",
            'admission_number': "Admission Number",
            'registration_number': "Registration Number",
            'department': "Department",
            'action': "Actions",
        }
        filter_criteria = {'active': True, 'data_verified': False}
        if 'a_number' in request.GET and request.GET['a_number']:
            filter_criteria['admission_number'] = request.GET['a_number']
        
        students_objs = Student.objects.filter(**filter_criteria).order_by('admission_number')
        paginator = Paginator(students_objs, 10)
        page = request.GET.get('page')
        students = paginator.get_page(page)
        context['headers'] = headers
        context['students'] = students
        return render(request, self.template_name, context)


class VerifiedStudentView(View):
    template_name = 'students/students.html'
    def get(self, request, *args, **kwargs):
        context = {'label': 'Students'}
        headers = {
            'name': "Name",
            'admission_number': "Admission Number",
            'registration_number': "Registration Number",
            'department': "Department",
            'action': "Actions",
        }
        filter_criteria = {'active': True, 'data_verified': True}
        if 'a_number' in request.GET and request.GET['a_number']:
            filter_criteria['admission_number'] = request.GET['a_number']
        
        students_objs = Student.objects.filter(**filter_criteria).order_by('admission_number')
        paginator = Paginator(students_objs, 10)
        page = request.GET.get('page')
        students = paginator.get_page(page)
        context['headers'] = headers
        context['students'] = students
        return render(request, self.template_name, context)


class StudentDetailView(View):
    template_name = 'students/student.html'
    def get(self, request, *args, **kwargs):
        try:
            context = {}
            student_id = kwargs.get('pk')
            student = Student.objects.filter(pk=student_id).first()
            context['student'] = student
            tc_application = TcApplication.objects.filter(student_id=student_id)
            exists = tc_application.exists()
            if exists:
                context['tc_application'] = tc_application.first()
            context['tc_exists'] = exists
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('students:students'))


class StudentEditView(View):
    template_name = 'students/edit_students.html'
    def get(self, request, *args, **kwargs):
        context = {}
        student_id = kwargs.pop('pk')
        student = Student.objects.filter(pk=student_id).first()
        form = StudentEditForm(instance=student)
        context['form'] = form
        context['label'] = "Edit Student"
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk=student_id).first()
        form = StudentEditForm(request.POST, instance=student)
        if request.POST.get('data_verified') == 'on' and form.is_valid():
            form.save()
            if request.POST.get('applytc') == 'Save and apply TC':
                return HttpResponseRedirect(reverse('tc:apply_tc', args=(student_id,)))
            else:
                return HttpResponseRedirect(reverse('students:students'))
        else:
            context = {'form': form, 'label': "Edit Student"}
            return render(request, self.template_name, context)


def save_imported_students(request):
    if request.method == "POST":
        students = request.POST.getlist('students')
        for student_data in students:
            student = Student(**student_data)
            student.save()
        return redirect(reverse('students:student_list'))

    return redirect(reverse('students:import_students'))
