from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from Auth.models import User
from django.conf import settings 

# Create your views here.
def render_to_pdf(template_src, context_dict= {}) : 
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)
    if not pdf.err : 
        return HttpResponse(result.getvalue(), content_type= 'application/pdf')
    return None 

def ViewPDF(request) : 
    pdf = render_to_pdf('pdf.html', {'name': 'lol'})
    return HttpResponse(pdf, content_type= 'application/pdf')

def DownloadPDF(request) : 
    pdf = render_to_pdf('pdf.html', {'name' : 'lol'})
    response = HttpResponse(pdf, content_type= "application/json")
    filename = f"Invoice_{12341231}.pdf"
    content = f"attachment; filename={filename}"
    response['Content-Disposition']= content 
    return response

def UsersPDF(request) : 
    pdf = render_to_pdf('users.html', {'users': User.objects.all(), 'root' : settings.MEDIA_ROOT})
    print(f"STATIC ROOT -> {settings.STATIC_ROOT}")
    print(f"MEDIA ROOT -> {settings.MEDIA_ROOT}")
    return HttpResponse(pdf, content_type= 'application/pdf')

def DownloadUsersPDF(request) : 
    pdf = render_to_pdf('users.html', {'users': User.objects.all()})
    response =  HttpResponse(pdf, content_type= "application/json")
    filename = f'Invoice_users.pdf'
    content = f'attachment; filename={filename}'
    response['Content-Disposition']=content 
    return response

def Index(request) : 
    return render(request, 'index.html', {'root': settings.MEDIA_ROOT})