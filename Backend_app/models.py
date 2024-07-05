from django.db import models

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.file_name

class DataRecord(models.Model):
    csv_file = models.ForeignKey(CSVFile, on_delete=models.CASCADE)
    json_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.json_data)
