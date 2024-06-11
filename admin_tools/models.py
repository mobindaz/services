from django.db import models

# Create your models here.
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=3,default='CM')
    #head = models.ForeignKey(
    #    Teacher, on_delete=models.CASCADE, blank=True, null=True)

    def dept_code(self):
        if not self.code:
            return ""
        return self.code

    def __str__(self):
        return str(self.code)


class AcademicSession(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return '{} - {}'.format(self.year, self.year + 1)


class Classroom(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    academicyear = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        unique_together = ['academicyear','department', 'semester']
        ordering = ['department', 'semester']
    def __str__(self):
        return '%sS%s' % ( self.department,self.semester)