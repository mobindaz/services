from django.contrib import admin
from .models import Student
# Register your models here.
class studentAdmin(admin.ModelAdmin):
    list_display = ('admission_number','name','registration_number','departmentname')
    search_fields = ('name', 'admission_number')
    list_filter = ('department__name',)
    def departmentname(self,obj):
        return obj.department.name
admin.site.register(Student,studentAdmin)