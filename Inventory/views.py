import io
from urllib import request, response
import zipfile
from PIL import Image
from PyPDF2 import DocumentInformation
from colorama import Style
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Outgoing
from django.http import HttpResponse
from .models import InventoryReport, Incoming, Outgoing
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from .models import Room, Building, ResponsiblePerson, Product_Category, Incoming, Outgoing, MonitoringScreen, InventoryReport , Brand
from .forms import RoomForm, BuildingForm, ResponsiblePersonForm, ProductCategoryForm, IncomingForm , BrandForm
import os
from django.conf import settings
from django.views.generic import CreateView, ListView
from reportlab.lib.pagesizes import A4
from .models import Incoming
from barcode import generate
from barcode.writer import ImageWriter
import tempfile
from django.conf import settings
import barcode
# views.py
from django.shortcuts import render, redirect
from .forms import OutgoingForm
from django.views.generic import CreateView
from .models import Outgoing
import tempfile

from django.core.files.storage import FileSystemStorage
from django.core.files import File
fs = FileSystemStorage(location=settings.MEDIA_ROOT)

# الصفحات الرئيسة
def home(request):
    return render(request, 'home.html')
#########################################################################333
# المنتجات
def home1(request):
    return render(request, 'home1.html')


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_create.html'
    success_url = reverse_lazy('Inventory:home1')

class RoomListView(ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'room_update.html'
    success_url = reverse_lazy('room_list')

class BuildingCreateView(CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'building_create.html'
    success_url = reverse_lazy('Inventory:home1')

class BuildingListView(ListView):
    model = Building
    template_name = 'building_list.html'
    context_object_name = 'buildings'

class BuildingUpdateView(UpdateView):
    model = Building
    form_class = BuildingForm
    template_name = 'building_update.html'
    success_url = reverse_lazy('building_list')

class ResponsiblePersonCreateView(CreateView):
    model = ResponsiblePerson
    form_class = ResponsiblePersonForm
    template_name = 'responsible_person_create.html'
    success_url = reverse_lazy('Inventory:home1')

class ResponsiblePersonListView(ListView):
    model = ResponsiblePerson
    template_name = 'responsible_person_list.html'
    context_object_name = 'persons'

class ResponsiblePersonUpdateView(UpdateView):
    model = ResponsiblePerson
    form_class = ResponsiblePersonForm
    template_name = 'responsible_person_update.html'
    success_url = reverse_lazy('responsible_person_list')

class ProductCategoryCreateView(CreateView):
    model = Product_Category
    form_class = ProductCategoryForm
    template_name = 'product_category_create.html'
    success_url = reverse_lazy('Inventory:home1')

class ProductCategoryListView(ListView):
    model = Product_Category
    template_name = 'product_category_list.html'
    context_object_name = 'categories'

class ProductCategoryUpdateView(UpdateView):
    model = Product_Category
    form_class = ProductCategoryForm
    template_name = 'product_category_update.html'
    success_url = reverse_lazy('product_category_list')

    ######
class BrandFormCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brand_create.html'
    success_url = reverse_lazy('Inventory:home1')
class BrandFormListView(ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'




##################################################################################################################
def home2(request):
    incomings = Incoming.objects.all() #  Mohamed Gamal edit get from models main table
    return render(request, 'home2.html', {'incomings': incomings}) #  add context Mohamed Gamal edit

class IncomingCreateView(CreateView):
    model = Incoming
    fields = ['product_category', 'brand', 'quantity', 'purchase_invoice', 'description']
    template_name = 'incoming_create.html'
    success_url = '/home2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # قم بتمرير الفئات والبراند المطلوبة إلى العرض
        context['categories'] = Product_Category.objects.all()  
        context['brands'] = Brand.objects.all()  
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.generate_barcode()
        return response

class IncomingListView(ListView):
    model = Incoming
    template_name = 'incoming_list.html'
    context_object_name = 'incomings'


def incomingdetail(request, pk):
    incoming = get_object_or_404(Incoming, pk=pk)
    return render(request, 'incoming_detail.html', {'incoming': incoming})

def print_barcode(request, pk):
    try:
        incoming = Incoming.objects.get(pk=pk)
        category = incoming.product_category.first()
        barcode_dir = os.path.join(settings.MEDIA_ROOT, 'barcode', category.slug)
        os.makedirs(barcode_dir, exist_ok=True)

        # Loop through each item in the incoming product quantity
        for i in range(incoming.quantity):
            barcode_filename = f'{incoming.pk}_{i+1}_barcode.png' # add unique identifier for each barcode
            barcode_path_filename = os.path.join(barcode_dir, barcode_filename)

            # Generate barcode
            barcode_data = f'{incoming.pk:06d}{i+1:02d}'.zfill(12) # add unique identifier for each barcode

            barcode_value = barcode.get('code128', barcode_data, writer=barcode.writer.ImageWriter())
            barcode_value.default_writer_options['module_width'] = 0.25 # adjust size of barcode
            barcode_value.default_writer_options['module_height'] = 5.0 # adjust size of barcode
            barcode_value.default_writer_options['quiet_zone'] = 10 # adjust size of quiet zone

            # Render the barcode to a BytesIO object
            barcode_buffer = io.BytesIO()
            barcode_value.write(barcode_buffer)
            barcode_buffer.seek(0)

            # Save the barcode as a PNG file
            with open(barcode_path_filename, 'wb') as barcode_file:
                barcode_file.write(barcode_buffer.read())

        # Create a zip file containing all the barcode PNGs
        zip_filename = f'{category.slug}_barcodes.zip'
        zip_path_filename = os.path.join(barcode_dir, zip_filename)
        with zipfile.ZipFile(zip_path_filename, 'w') as zip_file:
            for i in range(incoming.quantity):
                barcode_filename = f'{incoming.pk}_{i+1}_barcode.png'
                barcode_path_filename = os.path.join(barcode_dir, barcode_filename)
                zip_file.write(barcode_path_filename, barcode_filename)

        # Return the zip file as a response
        with open(zip_path_filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{category.slug}_barcodes.zip"'
            return response

    except Exception as e:
        return HttpResponse(f"An error occurred while generating and saving the barcodes: {str(e)}")



########################################################################################################################3
def home3(request):
    return render(request, 'home3.html')

from django.shortcuts import render, redirect
from django.views import View
from .models import Incoming
from .forms import OutgoingForm

class OutgoingListView(View):
    def get(self, request):
        return render(request, 'outgoing_list.html')
    
    def post(self, request):
        form = OutgoingForm(request.POST)
        if form.is_valid():
            barcode_number = form.cleaned_data['barcode_number']
            try:
                incoming = Incoming.objects.get(barcode_number=barcode_number)
            except Incoming.DoesNotExist:
                return render(request, 'outgoing_list.html', {'error': 'المنتج غير موجود'})
            
            if incoming.quantity <= 0:
                return render(request, 'outgoing_list.html', {'error': 'الكمية المتوفرة غير كافية'})
            
            incoming.quantity -= 1
            incoming.save()
            
            form.save()
            return redirect('outgoing_list')
        
        return render(request, 'outgoing_list.html', {'form': form})

from django.shortcuts import render, redirect
from django.views import View
from .models import Incoming
from .forms import OutgoingForm

class OutgoingCreateView(View):
    def get(self, request):
        form = OutgoingForm()
        return render(request, 'outgoing.html', {'form': form})
    
    def post(self, request):
        barcode_scanner_device = request.POST['barcode_scanner_device']
        try:
            incoming = Incoming.objects.get(barcode_number=barcode_scanner_device)
        except Incoming.DoesNotExist:
            form = OutgoingForm(request.POST)
            return render(request, 'outgoing.html', {'form': form, 'error': 'المنتج غير موجود'})
        
        if incoming.quantity <= 0:
            form = OutgoingForm(request.POST)
            return render(request, 'outgoing.html', {'form': form, 'error': 'الكمية المتوفرة غير كافية'})
        
        incoming.quantity -= 1
        if incoming.quantity == 0:
            incoming.delete()
        else:
            incoming.save()
        
        form = OutgoingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('outgoing_list')
        
        return render(request, 'outgoing.html', {'form': form})







#################################################################################################


from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum, Q
from .models import Product_Category, Incoming, Outgoing, MonitoringScreen

from django.shortcuts import get_object_or_404

class MonitoringScreenView(TemplateView):
    template_name = 'monitoring_screen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_category_id = self.request.GET.get('product_category_id')
        context['stock_history'] = None
        context['available_stock'] = None
        context['current_orders'] = None

        if product_category_id:
            product_category = get_object_or_404(Product_Category, id=product_category_id)
            monitoring_screen = MonitoringScreen.objects.get(product_category=product_category)

            # عرض حركة المخزون
            stock_history = monitoring_screen.display_inventory()

            # عرض الكمية المتاحة
            available_stock = monitoring_screen.available_stock()

            # عرض الطلبات الحالية
            current_orders = monitoring_screen.current_orders()

            context['product_category'] = product_category
            context['stock_history'] = stock_history
            context['available_stock'] = available_stock
            context['current_orders'] = current_orders

        return context



def search(request):
    if request.method == 'GET':
        category = request.GET.get('category', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        stock_items = Incoming.objects.none()
        if category:
            stock_items = Incoming.objects.filter(product_category__name__icontains=category) | Outgoing.objects.filter(product_category__name__icontains=category)

        if start_date and end_date:
            stock_items = stock_items.filter(Q(purchase_date__range=[start_date, end_date]) | Q(issue_date__range=[start_date, end_date]))

        context = {
            'stock_items': stock_items,
        }

        return render(request, 'search.html', context)
#################################################################################################

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import InventoryReport
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic import View
from xhtml2pdf import pisa
from io import BytesIO
from .models import InventoryReport

def inventory_report(request):
    reports = InventoryReport.objects.all()
    return render(request, 'inventory_report.html', {'reports': reports})

class ReportPDF(View):
    def get(self, request, report_id):
        report = get_object_or_404(InventoryReport, id=report_id)
        stock_items = report.get_stock_items()
        consumption_percentage = report.get_consumption_percentage()
        items_to_reorder = report.get_items_to_reorder(threshold=10)

        context = {
            'report': report,
            'stock_items': stock_items,
            'consumption_percentage': consumption_percentage,
            'items_to_reorder': items_to_reorder,
        }

        html = render_to_string('inventory_report_pdf.html', context)
        pdf = self.generate_pdf(html)
        return HttpResponse(pdf, content_type='application/pdf')

    def generate_pdf(self, html):
        pdf_file = BytesIO()
        pisa.CreatePDF(html, dest=pdf_file, encoding='UTF-8')
        pdf_file.seek(0)
        return pdf_file.read()

export_report_as_pdf = ReportPDF.as_view()
def generate_report(request, report_id):
    report = InventoryReport.objects.get(id=report_id)
    stock_items = report.get_stock_items()
    consumption_percentage = report.get_consumption_percentage()
    items_to_reorder = report.get_items_to_reorder(threshold=10)

    context = {
        'report': report,
        'stock_items': stock_items,
        'consumption_percentage': consumption_percentage,
        'items_to_reorder': items_to_reorder,
    }
    return render(request, 'report_details.html', context)

def export_report_as_pdf(request):
    report_id = request.GET.get('report_id')
    report = InventoryReport.objects.get(id=report_id)
    stock_items = report.get_stock_items()
    consumption_percentage = report.get_consumption_percentage()
    items_to_reorder = report.get_items_to_reorder(threshold=10)

    context = {
        'report': report,
        'stock_items': stock_items,
        'consumption_percentage': consumption_percentage,
        'items_to_reorder': items_to_reorder,
    }

    template_path = 'inventory_report_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="inventory_report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('An error occurred while creating the PDF.')

    return response



