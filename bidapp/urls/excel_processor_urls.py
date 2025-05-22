from django.urls import path
from ..apis.excel_processor import excel_processor

urlpatterns = [
    path('excel-processor/', excel_processor, name='excel_processor'),
]
