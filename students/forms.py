from django import forms
from .models import Student
from common.widgets import XDSoftDateTimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div,Button
from django.urls import reverse
from tc.models import TcApplication

class StudentEditForm(forms.ModelForm):

	class Meta:from django import forms
from .models import Student
from common.widgets import XDSoftDateTimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div,Button
from django.urls import reverse
from tc.models import TcApplication

class StudentEditForm(forms.ModelForm):

	class Meta:
		model = Student
		fields = ['admission_number','name',
		'gender','date_of_birth','department','guardian',
				  'guardian_relation','religion','community','category','date_of_join','feeconcession',
				  'data_verified','registration_number'
		]
		widgets={
			"date_of_birth" : forms.widgets.DateInput(attrs={'type': 'date'}),
			"date_of_join" : forms.widgets.DateInput(attrs={'type': 'date'})
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ['admission_number','name',
		'gender','date_of_birth','department','guardian',
			'guardian_relation','religion','community','category','date_of_join','registration_number','feeconcession',
			'data_verified',
		]
		buttons = {'save':'save'}
		exists = TcApplication.objects.filter(student_id=self.instance.pk).exists()
		if not exists:
			buttons['applytc'] = 'Save and apply TC'

		self.helper = FormHelper()
		self.helper.layout = Layout()
		done = False
		index= 0
		while index < len(fields):
			row = Row()
			row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
			index += 1
			if index < len(fields):
				row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
				index += 1
			if index < len(fields):
				row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
				index += 1
			row.css_class='form-row'
			self.helper.layout.append(row)
		
		for key,value in buttons.items():
			self.helper.layout.append(Submit(key,value))
		self.helper.layout.append(Button('cancel', 'Cancel', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('students:students'))))
		#it will looks like below
		# self.helper.layout = Layout(
		# 	Row(
		# 		Column('admission_number',css_class='form-group col-md-4 mb-0'),
		# 		Column('name',css_class='form-group col-md-4 mb-0'),
		# 		Column('gender',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Row(
		# 		Column('date_of_birth',css_class='form-group col-md-4 mb-0'),
		# 		Column('guardian',css_class='form-group col-md-4 mb-0'),
		# 		Column('guardian_relation',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Row(
		# 		Column('religion',css_class='form-group col-md-4 mb-0'),
		# 		Column('community',css_class='form-group col-md-4 mb-0'),
		# 		Column('category',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Row(
		# 		Column('department',css_class='form-group col-md-4 mb-0'),
		# 		Column('feeconcession',css_class='form-group col-md-4 mb-0'),
		# 		Column('data_verified',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Submit('save', 'save'),
		# 	Submit('cancel', 'cancel'),
		# 	Submit('applytc','Save and Apply TC')
		# )
		model = Student
		fields = ['admission_number','name',
		'gender','date_of_birth','department','guardian',
				  'guardian_relation','religion','community','category','date_of_join','feeconcession',
				  'data_verified','registration_number'
		]
		widgets={
			"date_of_birth" : forms.widgets.DateInput(attrs={'type': 'date'}),
			"date_of_join" : forms.widgets.DateInput(attrs={'type': 'date'})
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ['admission_number','name',
		'gender','date_of_birth','department','guardian',
			'guardian_relation','religion','community','category','date_of_join','registration_number','feeconcession',
			'data_verified',
		]
		buttons = {'save':'save'}
		exists = TcApplication.objects.filter(student_id=self.instance.pk).exists()
		if not exists:
			buttons['applytc'] = 'Save and apply TC'

		self.helper = FormHelper()
		self.helper.layout = Layout()
		done = False
		index= 0
		while index < len(fields):
			row = Row()
			row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
			index += 1
			if index < len(fields):
				row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
				index += 1
			if index < len(fields):
				row.append( Column(fields[index],css_class='form-group col-md-4 mb-0'))
				index += 1
			row.css_class='form-row'
			self.helper.layout.append(row)
		
		for key,value in buttons.items():
			self.helper.layout.append(Submit(key,value))
		self.helper.layout.append(Button('cancel', 'Cancel', css_class='btn-primary',
                             onclick="window.location.href = '{}';".format(reverse('students:students'))))
		#it will looks like below
		# self.helper.layout = Layout(
		# 	Row(
		# 		Column('admission_number',css_class='form-group col-md-4 mb-0'),
		# 		Column('name',css_class='form-group col-md-4 mb-0'),
		# 		Column('gender',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Row(
		# 		Column('date_of_birth',css_class='form-group col-md-4 mb-0'),
		# 		Column('guardian',css_class='form-group col-md-4 mb-0'),
		# 		Column('guardian_relation',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Row(
		# 		Column('religion',css_class='form-group col-md-4 mb-0'),
		# 		Column('community',css_class='form-group col-md-4 mb-0'),
		# 		Column('category',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Row(
		# 		Column('department',css_class='form-group col-md-4 mb-0'),
		# 		Column('feeconcession',css_class='form-group col-md-4 mb-0'),
		# 		Column('data_verified',css_class='form-group col-md-4 mb-0'),
		# 		css_class='form-row'
		# 	),
		# 	Submit('save', 'save'),
		# 	Submit('cancel', 'cancel'),
		# 	Submit('applytc','Save and Apply TC')
		# )