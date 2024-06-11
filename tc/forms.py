from .models import TcApplication,TcIssue
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import (Layout, Fieldset, Field,
                                 ButtonHolder, Submit, Div)
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Button
from django.urls import reverse
from datetime import datetime
from django.db.models import Max

class TcApplicationForm(ModelForm):
    class Meta:
        model = TcApplication
        fields = ['reasonforLeaving','dateofApplication','promotionDate','lastclass',
        'promotedtoHigherClass','proceedingInstitution','lastAttendedDate','attendance','totalWorkingDay','tc_application_Number','tc_application_Year'
        ]
        widgets={
            "dateofApplication" : forms.widgets.DateInput(attrs={'type': 'date'}),
            "promotionDate" : forms.widgets.DateInput(attrs={'type': 'date'}),
            "lastAttendedDate":forms.widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['reasonforLeaving','dateofApplication','promotionDate','lastclass',
                  'promotedtoHigherClass','proceedingInstitution','lastAttendedDate',
                  'attendance','totalWorkingDay'
        ]
        buttons = {'apply':'apply'}
        if 'instance' in kwargs:
            self.fields['tc_application_Number'] = forms.CharField(disabled=True,initial=self.instance.tcNumber,label="Application Number")
            self.fields['tc_application_Year'] = forms.CharField(disabled=True,initial=self.instance.tcYear,label="TC Application Year")
            fields.extend(['tc_application_Number','tc_application_Year'])
        else:
        #fill some default values 
            self.fields['totalWorkingDay'].initial = 78
            self.fields['lastAttendedDate'].initial = '2020-03-24'
            self.fields['promotionDate'].initial = '2019-11-27'
            self.fields['reasonforLeaving'].initial ='Course Completed'

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

    def clean(self,*args,**kwargs):
        tcApplicationNumber = TcApplication.objects.all().aggregate(Max ('tc_application_Number')) ['tc_application_Number__max']
        if tcApplicationNumber == None:
            tcApplicationNumber = 1
        else:
            tcApplicationNumber +=1          
        self.instance.tc_application_Number = tcApplicationNumber
        self.instance.tc_application_Year = datetime.now().year
        print("application number",self.instance.tc_application_Number)
        return super().clean(*args,**kwargs)

class TCIssueForm(ModelForm):
    class Meta:
        model = TcApplication
        fields = ['tcNumber','tcYear','conduct']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['tcNumber','tcYear','conduct']
        buttons = {'issuetc':'Issue TC'}
        #self.fields['tcNumber'] = forms.CharField(disabled=True,initial=self.instance.tcNumber,label="TC Number")
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
                             onclick="window.location.href = '{}';".format(reverse('tc:all_tc'))))

    def clean(self,*args,**kwargs):
        print ("Clean function called")
        tcApplicationNumber = TcApplication.objects.all().aggregate(Max ('tc_application_Number')) ['tc_application_Number__max']
        if tcApplicationNumber == None:
            tcApplicationNumber = 1
        else:
            tcApplicationNumber +=1          
        self.instance.tc_application_Number = tcApplicationNumber
        self.instance.tc_application_Year = datetime.now().year
        print("application number",self.instance.tc_application_Number)
        return super().clean(*args,**kwargs)     