from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    # Asistente
    path('checkout/<int:categoria_pk>/', views.CheckoutView.as_view(), name='checkout'),
    path('mis-entradas/', views.MyTicketsView.as_view(), name='my_tickets'),
    path('entrada/<uuid:codigo>/', views.TicketDetailView.as_view(), name='detail'),

    # Validación por QR (acceso público desde enlace del QR)
    path('validar/<uuid:codigo>/', views.ValidarQRView.as_view(), name='validar_qr'),

    # Check-in operador
    path('checkin/', views.CheckInView.as_view(), name='checkin'),
    path('api/validar/', views.ApiValidarView.as_view(), name='api_validar'),

    # Dashboard organizador
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/api/ventas/<int:evento_id>/', views.ApiVentasCategoriaView.as_view(), name='api_ventas'),
    path('dashboard/api/asistencia/<int:evento_id>/', views.ApiAsistenciaDiaView.as_view(), name='api_asistencia'),
    path('dashboard/exportar/<int:evento_id>/', views.ExportExcelView.as_view(), name='export_excel'),
]
