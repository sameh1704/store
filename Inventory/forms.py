
from django import forms
from .models import Room, Building, ResponsiblePerson, Product_Category, Brand, Incoming, Outgoing, MonitoringScreen, InventoryReport

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = '__all__'

class ResponsiblePersonForm(forms.ModelForm):
    class Meta:
        model = ResponsiblePerson
        fields = '__all__'

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = Product_Category
        fields = '__all__'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
########################################################################################################################3


class IncomingForm(forms.ModelForm):
    class Meta:
        model = Incoming
        fields = '__all__'



########################################################################################################################3


from django import forms
from .models import Outgoing

class OutgoingForm(forms.ModelForm):
    class Meta:
        model = Outgoing
        fields = ['product_category', 'brand', 'quantity', 'building', 'room', 'barcode_number']




########################################################################################################################3
class MonitoringScreenForm(forms.ModelForm):
    class Meta:
        model = MonitoringScreen
        fields = '__all__'

class MonitoringScreenForm(forms.ModelForm):
    class Meta:
        model = MonitoringScreen
        fields = '__all__'
########################################################################################################################3


from .models import InventoryReport

class InventoryReportForm(forms.ModelForm):
    class Meta:
        model = InventoryReport
        fields = ['start_date', 'end_date', 'product_category']


