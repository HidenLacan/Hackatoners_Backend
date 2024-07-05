from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CSVUploadView, DataRecordViewSet

router = DefaultRouter()
router.register(r'datarecords', DataRecordViewSet)

urlpatterns = [
    path('upload-csv/', CSVUploadView.as_view(), name='upload-csv'),
    path('api/', include(router.urls)),
]
