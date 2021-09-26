from django.urls import path, include
from rest_framework import routers
from .views import UploadViewSet

router = routers.DefaultRouter()
router.register('download/csv', UploadViewSet, basename="download_csv")
router.register('download/json', UploadViewSet, basename="download_json")
router.register('view/json', UploadViewSet, basename="view_json")

urlpatterns = [
    path('', include(router.urls)),
]