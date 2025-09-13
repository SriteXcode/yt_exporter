from django.urls import path
from . import views

app_name = 'playlist'

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download_csv, name='download_csv'),
]
