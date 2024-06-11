from django.shortcuts import render
from .forms import TcApplicationForm,TCIssueForm
from django.contrib.auth.decorators import login_required
from .models import TcApplication,TcIssue
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from admin_tools.models import Classroom
from reportlab.platypus import Paragraph
from django.db.models import Max
import num2words
from django.templatetags.static import static

from reportlab.platypus import PageBreak

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Max
import io
from django.http import FileResponse

from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT

from reportlab.lib.units import inch ,cm
from reportlab.lib.pagesizes import A4
rowhight = 1.4*cm
from students.models import Student
sample_style_sheet = getSampleStyleSheet()
# Create your views here.
paragraphstyle  = ParagraphStyle(
   'conduct',
    parent=sample_style_sheet['Normal'],
    fontSize=11,
    leading=14,
    alignment = TA_JUSTIFY,)
   
#@login_required
class  ApplyTcView(View):
    template_name = 'tc/apply_tc.html'
    def get(self,request,*args,**kwargs):
        context = {}
        initial = {}
        k_args = {}
        if kwargs == None:
            form = TcApplicationForm()
        else:
            primary_key = kwargs.get('pk')
            student = Student.objects.filter(pk = primary_key).first()
            instance = TcApplication.objects.filter(student=student).first()
            if instance:
                k_args['instance'] = instance
            form = TcApplicationForm(**k_args)
        context['form'] = form
        context['student'] = student
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        if 'apply' in request.POST and request.POST['apply'] != '':
            form = TcApplicationForm(request.POST)
            student_id = kwargs.get('pk')
            student = Student.objects.filter(pk = student_id).first()
            instance = TcApplication.objects.filter(student=student).first()
            #a new entry
            if instance == None:
                if form.is_valid():
                    #each year tc application number should be reset. finding the maximum number in the current year
                    current_year = datetime.now().year
                    tcApplicationNumber = TcApplication.objects.filter(tc_application_Year= current_year).aggregate(Max ('tc_application_Number')) ['tc_application_Number__max']
                    if tcApplicationNumber == None:
                        tcApplicationNumber = 1
                    else:
                        tcApplicationNumber +=1          
                    form.instance.tc_application_Number = tcApplicationNumber
                    form.instance.tc_application_Year = datetime.now().year
                    student = Student.objects.filter(pk=student_id).first()
                    student_id = student.id
                    application = form.save(commit=False)
                    application.student = student
                    application.save()
                else:
                    context = {}
                    context['form'] = form
                    return render(request,self.template_name,context)
            # edit request
            else:
                k_args = {}
                k_args['instance'] = instance
                form = TcApplicationForm(request.POST,**k_args)
                student_id = instance.student.id
                if form.is_valid():
                    form.save()
                else:
                    context = {}
                    context['form'] = form
                    return render(request,self.template_name,context)

            return HttpResponseRedirect(reverse('students:student',args=(student_id,)))

class  EditTcView(View):
    template_name = 'tc/apply_tc.html'
    def get(self,request,*args,**kwargs):
        context = {}
        initial = {}
        k_args = {}
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk = student_id).first()
        instance = TcApplication.objects.filter(student=student).first()
        if instance:
            k_args['instance'] = instance
        form = TcApplicationForm(**k_args)
        context['form'] = form
        return render(request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        if 'apply' in request.POST and request.POST['apply'] != '':
            k_args = {}
            student_id = kwargs.get('pk')
            student = Student.objects.filter(pk = student_id).first()
            instance = TcApplication.objects.filter(student=student).first()
            if instance:
                k_args['instance'] = instance
            form = TcApplicationForm(request.POST,**k_args)
            if form.is_valid():
                form.save()
            else:
                context = {}
                context['form'] = form
                return render(request,self.template_name,context)
            return HttpResponseRedirect(reverse('tc:all_tc'))
        if 'cancel' in request.POST and request.POST['cancel'] != '':
            return HttpResponseRedirect(reverse('tc:all_tc'))

class  CancelTcView(View):
    template_name = 'tc/apply_tc.html'
    def get(self,request,*args,**kwargs):
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk = student_id).first()
        TcApplication.objects.filter(student=student).delete() 
        return HttpResponseRedirect(reverse('tc:all_tc'))


def application_all_view(request):
    tcapplications = TcApplication.objects.filter(tc_issued = False).order_by('id').reverse()
    for tcapplication in tcapplications:
        tcapplication.activeclassroom = Classroom.objects.filter(student = tcapplication.student,active=True).first()
    return render(request, 'tc/tc_applications_all.html', {'tcapplications':tcapplications})
    
def tcissued_all_view(request):
    tcapplications = TcApplication.objects.filter(tc_issued = True).order_by('tcYear','tcNumber').reverse()
    return render(request, 'tc/tc_issued_all.html', {'tcapplications':tcapplications})

def tc_application_by_department_view(request, pk):
    dept_name = Department.objects.get(pk=pk)
    tcapplications = TcApplication.objects.filter(department=dept_name)
    for tcapplication in tcapplications:
        tcapplication.activeclassroom = Classroom.objects.filter(student = tcapplication.student,active=True)
        print(tcapplication.student,tcapplication.activeclassroom)
    return render(request, 'tc/tc_applications_by_department.html', tcapplications)

def printtable_in_doc(elements,data,style=1):   
    if(style == 1):
        table = Table(data, colWidths=270 )
    else:
        table = Table(data, colWidths=270/2,rowHeights=rowhight ) 
    tablestyle =   TableStyle([
    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('TOPPADDING',(0,0),(-1,-1),5),
    #('SPAN',(-2,-1),(-1,-1)),
    ('VALIGN', (0, 0), (1, 0), 'MIDDLE'),
    ('FONTSIZE',(0,0),(-1,-1),11),
    ])
    table.setStyle(tablestyle)
    elements.append(table  )
def print_conductCertificate(elements,student):
    conductstyle  = ParagraphStyle(
   'conduct',
    parent=sample_style_sheet['Normal'],
    fontSize=12,
    leading=14,
    alignment = TA_JUSTIFY,)
    heading = 'COURSE AND CONDUCT CERTIFICATE'
    print_heading(elements,heading)
    date_of_join = student.date_of_join.strftime("%d/%m/%Y")
    lastAttendedDate = student.lastAttendedDate.strftime("%d/%m/%Y")
    lastMonth = student.lastAttendedDate.strftime("%B")
    lastYear = student.lastAttendedDate.strftime("%Y")
    print (student.reasonforLeaving)
    if student.reasonforLeaving == "Course Completed" :
        data = [ Paragraph ("Certified that Shri/Kumari <b>"+student.name +"</b>  was a student in this institution of "+ student.department.name +" department from " + date_of_join + " to "+ lastAttendedDate + " and he/she completed his/her 3 year diploma programme of study in "+lastMonth + " " + lastYear +". The medium of the entire programme was English. <br/><br/> During the course of study his/her character and conduct were found <b> Good </b> <br/><br/> Place : Palakkad<br/> Date : "+student.dateofissue ,conductstyle )]
    else:
        data = [ Paragraph ("Certified that Shri/Kumari <b>"+student.name +"</b>  was a student in this institution of "+ student.department.name +" department from " + date_of_join + " to "+ lastAttendedDate + ".<br/><br/> During the course of study his/her character and conduct were found <b> Good </b> <br/> Place : Palakkad <br/> Date : "+student.dateofissue,conductstyle )]
    data = [data]

    table = Table(data, colWidths=270*2) 
    #command ,startindex ,endindex 
    tablestyle =   TableStyle([
    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ('BOTTOMPADDING',(0,0),(-1,-1),20),
    ('TOPPADDING',(0,0),(-1,-1),5),
    ('FONTSIZE',(0,0),(-1,-1),20),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(tablestyle)
    elements.append(table  )

def print_heading(elements,heading):
    sample_style_sheet = getSampleStyleSheet()
    title_style = sample_style_sheet['Heading3']
    title_style.alignment = 1
    paragraph_1 = Paragraph(heading,title_style )
    elements.append(paragraph_1)


def prepareTCApplication(tcapplication):
        
        heading = ' GOVERNMENT POLYTECHNIC COLLEGE, PALAKKAD <br/>\
                            APPLICATION FOR ISSUING T.C , COURSE AND CONDUCT \
                            CERTIFICATE AND SSLC BOOK '
        elements = []
        print_heading(elements,heading)
        periodofstudy = tcapplication.student.date_of_join.strftime("%d/%m/%Y") + " to "+tcapplication.lastAttendedDate.strftime("%d/%m/%Y")
        if tcapplication.student.feeconcession == True:
            feeconcession = "Yes"
        else:
            feeconcession = "No"
        
        data = [
            ('Application No',str(tcapplication.tc_application_Number) + " / "+ str(tcapplication.tc_application_Year) ),
            ('Department',tcapplication.student.department.name),
            ('Last enrolled class',tcapplication.lastclass),
            ('Admission No',tcapplication.student.admission_number),
            ('Name of the student',tcapplication.student.name),
            ("Name of Guardian",
                tcapplication.student.guardian+ ","+ tcapplication.student.guardian_relation),
            ('Period Of Study',periodofstudy),
            ('Date of birth',tcapplication.student.date_of_birth.strftime("%d/%m/%Y")),
            ("Religion and Community", tcapplication.student.religion +","+tcapplication.student.community),
            ('Whether the pupil was in receipt of fee concession',feeconcession),
            ('Reason for leaving',tcapplication.reasonforLeaving),
            ('Signature of the applicant with date',"")
        ]

        printtable_in_doc(elements,data)

        
        paragraph_1 = Paragraph("Dues if any to be furnished below",sample_style_sheet['Heading3'])
        elements.append(paragraph_1  )
        data  = [
            ("Section","Signature & Name","Section","Signature & Name"),
            ("Head of section","","Workshop",""),
            ("Applied Science lab","","Library",""),
            ("Co-op Society","","Physical education",""),
            ("NSS","","NCC",""),
            ("Hostel","","Academic section",""),
        ]

        printtable_in_doc(elements,data,style=2)
        data = [
            ("Date of pupil's last attendance at Institution",tcapplication.lastAttendedDate.strftime("%d/%m/%Y")),
            ("Total No of working days",tcapplication.totalWorkingDay),
            ("No.of working days the pupil attended",tcapplication.attendance),
            ("Date of application",tcapplication.dateofApplication.strftime("%d/%m/%Y")),
            ("Signature of tutor",""),
            ("Head of Section","")
        ]
        printtable_in_doc(elements,data)
        return elements
class  printTCApplication(View):
    def get(self,request,*args,**kwargs):
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk = student_id).first()
        tcapplication = TcApplication.objects.filter(student=student).first()
        filename = str(tcapplication.student.admission_number) + "-application.pdf"
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        
        doc.mytype="application"
        elements = prepareTCApplication(tcapplication)
        doc.topMargin = 1*cm
        doc.build(elements, onFirstPage=AllPageSetup, onLaterPages=AllPageSetup)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=filename)


class  printAllPendingApplications(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        tcapplications = TcApplication.objects.filter(tc_issued = False).order_by('student__department','student__name')
        filename = "All-application.pdf"
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        doc.topMargin = 1*cm
        elements =[]
        for application in tcapplications:
            elements.extend(prepareTCApplication(application))
            elements.append(PageBreak())
        doc.build(elements, onFirstPage=AllPageSetup, onLaterPages=AllPageSetup)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=filename)

def AllPageSetup(canvas, doc):
    canvas.saveState()
    filename= '/var/www/services/staticfiles/images/poly-logo-2.png'
    #filename= 'static/images/poly-logo-2.png'
    url = static('images/poly-logo-2.png')
    print("image url",url)
    canvas.drawImage(filename,A4[0]/3 -1.73*cm,A4[1]/3,width=A4[0]/2,height=A4[1]/2,mask='auto',preserveAspectRatio=True, anchor='c')
    #canvas.roundRect(x, y, width, height, radius, stroke=1, fill=0) 
    margin = .2 *cm
    canvas.roundRect(margin, margin, A4[0]-margin*2, A4[1]-margin*2, 1*cm, fill=0)
    margin = .2 *cm + .05*cm
    canvas.roundRect(margin, margin, A4[0]-margin*2, A4[1]-margin*2, 1*cm, fill=0)

    #printing principal tag in TC and CC, sicne its table style right alignment was difficult
    if hasattr(doc,"mytype"):
        if( doc.mytype == "tc"):
            canvas.drawRightString(A4[0] - 3*cm , 7*cm , "Principal")
            canvas.drawRightString(A4[0] - 3*cm , 2 *cm , "Principal")
            

    canvas.restoreState()

def  prepareTC(tcapplication):
    elements = []
    admission_number = tcapplication.student.admission_number
    filename = str(tcapplication.student.admission_number) + "-application.pdf"
    buffer = io.BytesIO()

    student = Student.objects.filter(admission_number=admission_number)[0]
    heading = """GOVERNMENT POLYTECHNIC COLLEGE PALAKKAD"""
           
    print_heading(elements,heading)
    heading = """TRANSFER CERTIFICATE"""
    print_heading(elements,heading)
    if (tcapplication.student.feeconcession == True):
        feeconcession = 'Yes'
    else:
        feeconcession = 'No'

    #date of birth in words 
    datofbirth = student.date_of_birth.strftime("%d/%m/%Y")
    year = student.date_of_birth.year
    month = student.date_of_birth.strftime("%B")
    date = student.date_of_birth.strftime("%d") 
    dateofissue = tcapplication.dateofIssue.strftime("%d/%m/%Y")
    dateofApplication = tcapplication.dateofApplication.strftime('%d/%m/%Y')
    promotionDate = tcapplication.promotionDate.strftime('%d/%m/%Y')
    lastAttendedDate = tcapplication.lastAttendedDate.strftime('%d/%m/%Y')
    tcapplication.dateofremovedfromrolls = tcapplication.lastAttendedDate
    dateofremovedfromrolls = tcapplication.dateofremovedfromrolls.strftime('%d/%m/%Y')
    dobinwords = Paragraph (
        (datofbirth + " " 
        + num2words.num2words(date,to='ordinal' ) + " " 
        + month + " " 
        + num2words.num2words(year)).title() ,
            sample_style_sheet['Normal'])

    lastclass = num2words.num2words( tcapplication.lastclass ,to='ordinal' ).title() 
    lastclass += " Semester " +  student.department.name
    tcdata = [
    ("TC Number : "+ str(tcapplication.tcNumber)+"/"+str(tcapplication.tcYear),"Admission Number : "+ str(admission_number)),
    ("Name of Educational Institution","Government Polytechnic College Palakkad"),
    ("Name of Pupil",student.name),
    ("Name of Guardian with the relationship with the pupil",
                student.guardian+ ","+student.guardian_relation),
    ("Nationality","Indian"),
    ("Religion and Community", student.religion +","+student.community),
    (Paragraph ("""Whether the candidate belongs to scheduled castes or
    scheduled tribes or other backward communities or whether
    he/or she converted from scheduled castes or
    Other backward Caste scheduled tribes""",paragraphstyle),student.category),
    ("Date of Birth according to admission Register", dobinwords),
    ("Class to which the pupil was last enrolled",lastclass),
    ("Date of Admission or promotion to that class",promotionDate),
    ("Whether qualified for promotion to a higher standard",tcapplication.promotedtoHigherClass),
    (Paragraph("Whether the pupil has paid all the fee due to the institution",sample_style_sheet['Normal']),'Yes'),
    ("Whether the pupil was in receipt of fee concession",feeconcession),
    ("Date of pupil's last attendance",lastAttendedDate),
    ("Date on which the name was removed from the rolls",dateofremovedfromrolls),
    ("No of working days up to the date",tcapplication.totalWorkingDay),
    ("No.of working days the pupil attended",tcapplication.attendance),
    ("Date of application for the certificate",dateofApplication),
    ("Date of issue of the certificate",dateofissue),
    ("Institution to which the pupil intends proceeding",tcapplication.proceedingInstitution),
    ("Prepared by (Section Clerk - Syam Kumar P)",""),
    ("Verified by (Junior Superintendent - Roy .M.J)",""),
    (Paragraph ("Date : " +dateofissue +"<br/>Place: Palakkad ",sample_style_sheet['Normal']), "" )
    #("Place: Palakkad","")
    ]
    printtable_in_doc(elements,tcdata)

    student.conduct = tcapplication.conduct
    student.lastAttendedDate = tcapplication.lastAttendedDate
    student.reasonforLeaving = tcapplication.reasonforLeaving
    student.dateofissue = dateofissue
    print_conductCertificate(elements,student)
    return elements

class tcIssue(View):
    template_name = "tc/issue_tc.html"
    def get(self,request,*args,**kwargs):
        #get the TC number

        pk = kwargs.get('pk')
        context = {}
        initial = {}
        k_args = {}
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk = student_id).first()
        instance = TcApplication.objects.filter(student=student).first()

        if instance.tcNumber == None: 
            current_year = datetime.now().year
            tcNumber = TcApplication.objects.filter(tcYear= current_year).aggregate(Max ('tcNumber')) ['tcNumber__max']
            if tcNumber == None:
                tcNumber = 1
            else:
                tcNumber +=1 
            instance.tcNumber = tcNumber
            instance.tcYear =current_year
        if instance:
            k_args['instance'] = instance

        form = TCIssueForm(**k_args)
        context['form'] = form
        context['student'] = instance.student
        return render(request,self.template_name,context)
 #       return response
    def post(self,request,*args,**kwargs):
        student_id = kwargs.get('pk')
        student = Student.objects.filter(pk = student_id).first()
        tcapplication = TcApplication.objects.filter(student=student).first()
        
        marktcIssued(tcapplication,request.POST.get('tcNumber'),request.POST.get('tcYear'))

        student_id  = tcapplication.student.id
        return HttpResponseRedirect(reverse('students:student',args=(student_id,)))
def getNextTCnumber():
    current_year = datetime.now().year
    tcNumber = TcApplication.objects.filter(tcYear= current_year).aggregate(Max ('tcNumber')) ['tcNumber__max']
    if tcNumber == None:
        tcNumber = 1
    else:
        tcNumber +=1
    return tcNumber
def marktcIssued(tcapplication,tcNumber=None,tcyear=None):
    if tcNumber == None:
        tcNumber = getNextTCnumber()
        tcyear = datetime.now().year
    if tcyear == None:
        tcyear = datetime.now().year
    tcapplication.tcNumber = tcNumber
    tcapplication.tcYear = tcyear
    tcapplication.tc_issued = True
    tcapplication.save()
    
class printTC(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        elements=[]
        student_id = pk
        student = Student.objects.filter(pk = student_id).first()
        tcapplication = TcApplication.objects.filter(student=student).first()
        filename = str(tcapplication.student.admission_number) + "-application.pdf"
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        doc.bottomMargin = .5*cm
        doc.topMargin = .75*cm
        doc.mytype="tc"
        elements =  prepareTC(tcapplication)
        doc.build(elements, onFirstPage=AllPageSetup, onLaterPages=AllPageSetup)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=filename)
class  IssueprintAllPendingApplications(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        tcapplications = TcApplication.objects.filter(tc_issued = False,student__data_verified = True).order_by('student__admission_number')
        filename = "All-TC.pdf"
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)
        doc.bottomMargin = .5*cm
        doc.topMargin = .75*cm
        doc.mytype="tc"
        elements =[]
        for application in tcapplications:
            marktcIssued(application)
            elements.extend(prepareTC(application))
            elements.append(PageBreak())
        doc.build(elements, onFirstPage=AllPageSetup, onLaterPages=AllPageSetup)
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=filename)
       

        