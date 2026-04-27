from django.urls import path

from . import views

app_name = "contracts"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("upload/", views.upload, name="upload"),
    path("<int:pk>/", views.detail, name="detail"),
]
