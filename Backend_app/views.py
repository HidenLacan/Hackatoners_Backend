import os
import csv
import json
import uuid
from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from django.http import JsonResponse
from .models import DataRecord, CSVFile
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
            # Generar un nombre único para el archivo
            file_name = f"{uuid.uuid4().hex}_{csv_file.name.split('.')[0]}"

            # Guardar el archivo CSV en el modelo CSVFile
            csv_file_instance = CSVFile.objects.create(file=csv_file, file_name=file_name)
            
            # Crear una carpeta única para este archivo CSV
            unique_folder = os.path.join(settings.MEDIA_ROOT, 'csv_files', file_name)
            os.makedirs(unique_folder, exist_ok=True)

            data_records = []
            try:
                # Leer y procesar el archivo CSV
                csv_file.seek(0)
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                print(f"Archivo decodificado: {decoded_file}")  # Depuración: Verificar el contenido del archivo
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    if row:  # Verificar si la fila no está vacía
                        data_records.append(row)
                        # Guardar cada fila como instancia de DataRecord con datos JSON
                        DataRecord.objects.create(csv_file=csv_file_instance, json_data=row)
                
                # Guardar el archivo JSON en la carpeta única
                json_file_path = os.path.join(unique_folder, f"{file_name}.json")
                with open(json_file_path, 'w') as json_file:
                    json.dump(data_records, json_file)
                
                # Comprobación de depuración
                print(f"Registros guardados: {data_records}")

                return JsonResponse({"status": "success", "data": data_records}, status=201)
            except Exception as e:
                print(f"Error al procesar el archivo CSV: {e}")
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
        else:
            print(f"Errores en el formulario: {form.errors}")
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

class DataRecordViewSet(viewsets.ModelViewSet):
    queryset = DataRecord.objects.all()
    serializer_class = DataRecordSerializer
