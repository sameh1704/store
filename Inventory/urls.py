from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import outgoingListView
from Inventory import views 
from .views import *




app_name = 'Inventory'

urlpatterns = [
    path('', views.home, name='home'),

    path('home1/', views.home1, name='home1'),
    #path('room/create/', RoomCreateView.as_view(), name='room_create'),
    #path('room/list/', RoomListView.as_view(), name='room_list'),
    #path('room/update/<int:pk>/', RoomUpdateView.as_view(), name='room_update'),
    ####################################################################################################################
    path('home1/building/create/', BuildingCreateView.as_view(), name='building_create'),
    path('building/list/', BuildingListView.as_view(), name='building_list'),
    path('building/update/<int:pk>/', BuildingUpdateView.as_view(), name='building_update'),
    ####################################################################################################################
    path('home1/responsible_person/create/', ResponsiblePersonCreateView.as_view(), name='responsible_person_create'),
    path('home1/responsible_person/list/', ResponsiblePersonListView.as_view(), name='responsible_person_list'),
    path('home1/responsible_person/update/<int:pk>/', ResponsiblePersonUpdateView.as_view(), name='responsible_person_update'),
    ####################################################################################################################
    path('home1/product_category/create/', ProductCategoryCreateView.as_view(), name='product_category_create'),
    path('home1/product_category/list/', ProductCategoryListView.as_view(), name='product_category_list'),
    path('home1/product_category/update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='product_category_update'),
    path('home1/brand/create/', BrandFormCreateView.as_view(), name='brand_create'),
    path('home1/brand/list/', BrandFormListView.as_view(), name='brand_list'),
   ####################################################################################################################
    path('home2/', views.home2, name='home2'),
    path('home2/incoming/create/', IncomingCreateView.as_view(), name='incoming_create'), 
    path('home2/incoming/', IncomingListView.as_view(), name='incoming_list'),
    path('home2/incoming/<int:pk>/', views.incomingdetail, name='incoming_detail'), # Mohamed Gamal edit
    path('home2/incoming/print_barcode/<int:pk>/', views.print_barcode, name='print_barcode'),
    #########################################################################################################3
    path('home3/', views.home3, name='home3'),
    #path('home3/outgoing/', outgoing_list, name='outgoing_list'),
    #path('home3/outgoing_add/', OutgoingCreateView.as_view(), name='outgoing_add'),
    path('home3/outgoing/', views.outgoing, name='outgoing'),
 
    ####################################################################################################################
    path('monitoring/', MonitoringScreenView.as_view(), name='monitoring_screen'),
    path('search/', views.search, name='search'),
    #######################################################################
    path('home/inventory/report/', views.inventory_report, name='inventory_report'),
    path('home/inventory/report/generate/<int:report_id>/', views.generate_report, name='generate_report'),
    path('home/inventory/report/export/pdf/', views.export_report_as_pdf, name='export_report_as_pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
