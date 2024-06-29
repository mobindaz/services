from django.db import models
from django.contrib.auth.models import User
from admin_tools.models import Department, AcademicSession,Classroom
# Create your models here.
relationship_type = (
    ('father','father'),
    ('mother','mother'),
    ('uncle','uncle'),
    )

gender_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class UploadedFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students',
                              default='studentavar.png',null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    admission_number = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=gender_choice, default='Male')
    registration_number = models.CharField(max_length=12, unique=True,null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    mobile = models.CharField(max_length=13, blank=True, null=True)
    guardian = models.CharField(max_length=100,default='')
    guardian_relation =  models.CharField(max_length=100,default='Father',choices = relationship_type )
    guardian_mobile = models.CharField(max_length=13, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_join = models.DateField(default='1998-01-01')
    religion = models.CharField(max_length=20,null=True)
    community = models.CharField(max_length=50,null=True)
    classroom = models.ManyToManyField(Classroom,blank=True)
    address = models.TextField(null=True)
    category = models.CharField(max_length = 30,null=True) 
    feeconcession = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    data_verified = models.BooleanField(default=False)

    def __str__(self):
        return '{} ({})-{}'.format(
            self.name, self.admission_number,self.department.name )
    class Meta:
        ordering = ['admission_number','department']