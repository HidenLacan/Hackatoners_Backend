import csv
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from django.http import JsonResponse
from .models import DataRecord
from .serializers import DataRecordSerializer
from .forms import CSVUploadForm

class CSVUploadView(View):
    def get(self, request):
        form = CSVUploadForm()
        return render(request, 'upload_csv.html', {'form': form})

    def post(self, request):
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            
            data_records = []
            # Leer el archivo subido directamente sin intentar acceder a su nombre
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                data_records.append(row)
                # Guardar cada fila como instancia de DataRecord con datos JSON
                DataRecord.objects.create(json_data=row)

            return JsonResponse({"status": "success", "data": data_records}, status=201)
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

class DataRecordViewSet(viewsets.ModelViewSet):
    queryset = DataRecord.objects.all()
    serializer_class = DataRecordSerializer
