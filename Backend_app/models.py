from django.db import models

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class DataRecord(models.Model):
    json_data = models.JSONField()  # Campo JSON para almacenar los datos
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.json_data)
