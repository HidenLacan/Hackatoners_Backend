from django.contrib import admin
from .models import DataRecord, CSVFile

@admin.register(DataRecord)
class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    search_fields = ('json_data',)
    readonly_fields = ('created_at',)

@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')
    search_fields = ('file',)
    readonly_fields = ('uploaded_at',)
