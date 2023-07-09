import os
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from autoslug import AutoSlugField
from barcode import generate
from barcode.writer import ImageWriter


fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Building(models.Model):
    BUILDING_CHOICES = (
        ('الامريكية', 'الامريكية'),
        ('رياض اطفال', 'رياض اطفال'),
        ('تمهيدى', 'تمهيدى'),
        ('ابتدائى ابو بكر', 'ابتدائى ابو بكر'),
        ('ابتدائى معاذ', 'ابتدائى معاذ'),
        ('اعدادى', 'اعدادى'),
        ('الادارة', 'الادارة'),
    )
    name = models.CharField(max_length=100, choices=BUILDING_CHOICES)
    rooms = models.ManyToManyField(Room)

    def __str__(self):
        return self.name



class ResponsiblePerson(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product_Category(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photo', default='download.png')
    slug = AutoSlugField(populate_from='name', unique=False)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Product_Category, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return self.name


def get_barcode_path(instance, filename):
    category_names = '-'.join([category.name for category in instance.product_category.all()])
    incoming_id = instance.id
    return os.path.join('product_barcodes', category_names, str(incoming_id), f'{instance.pk}_{filename}.pdf')

class Incoming(models.Model):
    product_category = models.ManyToManyField(Product_Category, related_name='incomings')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='incomings')
    quantity = models.PositiveIntegerField()
    purchase_invoice = models.ImageField(upload_to='purchase_invoices/')
    purchase_date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def generate_barcode(self):
        try:
            for category in self.product_category.all():
                for i in range(self.quantity):
                    barcode_data_i = f'{self.pk}{i:02d}'
                    barcode_path = os.path.join(settings.MEDIA_ROOT, 'product_barcodes', category.slug)
                    os.makedirs(barcode_path, exist_ok=True)
                    barcode_filename = f'{self.pk}_{i}_barcode.pdf'
                    barcode_path_filename = os.path.join(barcode_path, barcode_filename)
                    # Create PDF canvas
                    c = canvas.Canvas(barcode_path_filename, pagesize=A4)
                    # Generate barcode
                    barcode_value = generate('ean13', barcode_data_i, writer=ImageWriter())
                    barcode_value.drawOn(c, 10, 10)
                    # Save the PDF file
                    c.save()
        except Exception as e:
            print(f"An error occurred while generating and saving the barcode: {str(e)}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_barcode()
########################################################################################################################3

class Outgoing(models.Model):
    product_category = models.ManyToManyField(Product_Category, related_name='outgoing')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='outgoing')
    quantity = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    responsible_person = models.ForeignKey(ResponsiblePerson, on_delete=models.CASCADE)
    barcode_number = models.CharField(max_length=100)
    issue_date = models.DateField(default=timezone.now)
    


    def __str__(self):
        return f"Outgoing: {self.quantity} {self.product_category.name}"


    def save(self, *args, **kwargs):
        # استخدام الباركود المقروء للبحث عن المنتج المراد صرفه في قاعدة البيانات والتحقق من توفره وكميته
        try:
            incoming_product = Incoming.objects.get(barcode=self.barcode)
            if incoming_product.quantity >= self.quantity:
                # قم بتحديث كمية المنتج المتوفرة في قاعدة البيانات
                incoming_product.quantity -= self.quantity
                incoming_product.save()
            else:
                # نفدت الكمية بالكامل، قم بحذف السجل
                incoming_product.delete()
                raise Exception('لا يوجد كمية كافية من المنتج للصرف')
        except Incoming.DoesNotExist:
            raise Exception('المنتج غير متوفر في قاعدة البيانات')

        super(Outgoing, self).save(*args, **kwargs)
########################################################################################################################



    
class MonitoringScreen(models.Model):
    product_category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def display_inventory(self):
        # عرض حركة الوارد
        incoming_items = Incoming.objects.filter(product_category=self.product_category)
        for item in incoming_items:
            print(f"وارد: المنتج {item.product_category.name} بكمية {item.quantity} تم شراؤه في {item.purchase_date}")

        # عرض حركة المنصرف
        outgoing_items = Outgoing.objects.filter(product_category=self.product_category)
        for item in outgoing_items:
            print(f"منصرف: المنتج {item.product_category.name} بكمية {item.quantity} تم شراؤه في {item.issue_date}")

    def current_stock(self):
        incoming_items = Incoming.objects.filter(product_category=self.product_category)
        outgoing_items = Outgoing.objects.filter(product_category=self.product_category)

        total_incoming = sum([item.quantity for item in incoming_items])
        total_outgoing = sum([item.quantity for item in outgoing_items])
        current_stock = total_incoming - total_outgoing
        return current_stock

    def available_stock(self):
        incoming_items = Incoming.objects.filter(product_category=self.product_category)
        outgoing_items = Outgoing.objects.filter(product_category=self.product_category)
        total_incoming = sum([item.quantity for item in incoming_items])
        total_outgoing = sum([item.quantity for item in outgoing_items])
        available_stock = total_incoming - total_outgoing - self.current_orders()
        return available_stock

  

########################################################################################################################

class InventoryReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    product_category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)

    def get_stock_items(self):
        stock_items = Incoming.objects.filter(purchase_date__range=(self.start_date, self.end_date))
        return stock_items

    def get_consumption_percentage(self):
        total_quantity = Outgoing.objects.filter(product_category=self.product_category).aggregate(
            total_quantity=models.Sum('quantity')).get('total_quantity', 0)
        total_incoming_quantity = Incoming.objects.filter(product_category=self.product_category).aggregate(
            total_incoming_quantity=models.Sum('quantity')).get('total_incoming_quantity', 0)
        if total_incoming_quantity > 0:
            consumption_percentage = (total_quantity / total_incoming_quantity) * 100
        else:
            consumption_percentage = 0
        return consumption_percentage

    def get_items_to_reorder(self, threshold):
        reorder_items = Incoming.objects.filter(quantity__lte=threshold,
                                                purchase_date__range=(self.start_date, self.end_date))
        return reorder_items

    def export_report_as_pdf(self):
        # Prepare the document and its formatting
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        # Add the document title and format it
        styles = getSampleStyleSheet()
        report_title = "تقرير المخزون"
        title = Paragraph(report_title, styles['Heading1'])
        elements.append(title)
        # Add space after the title
        elements.append(Spacer(1, 0.5 * inch))
        # Add stock details
        stock_details = "تفاصيل المخزون:"
        elements.append(Paragraph(stock_details, styles['Heading2']))
        # Call the function to retrieve stock items
        stock_items = self.get_stock_items()
        # Format the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Create and format the table
        stock_table = Table(stock_items)
        stock_table.setStyle(table_style)
        elements.append(stock_table)
        # Add the consumption percentage
        consumption_percentage = self.get_consumption_percentage()
        percentage_text = f"نسبة الاستهلاك: {consumption_percentage}%"
        percentage = Paragraph(percentage_text, styles['Normal'])
        elements.append(percentage)
        # Add the items to reorder
        items_to_reorder = self.get_items_to_reorder()
        reorder_details = "العناصر التي تحتاج إلى إعادة طلبها:"
        elements.append(Paragraph(reorder_details, styles['Heading2']))
        for item in items_to_reorder:
            item_name = item.name
            reorder_item_details = f"- {item_name}"
            elements.append(Paragraph(reorder_item_details, styles['Normal']))
        # Build the document
        doc.build(elements)
        return response



