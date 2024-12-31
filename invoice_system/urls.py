# invoice_system/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoicing/', include('invoice.urls')),
    path('invoicing-by-pdf/', include('invoice_by_pdf.urls')),
]
