from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hospitals/', views.find_hospitals, name='find_hospitals'),
    path('distance/', views.calculate_distance, name='calculate_distance'),
]
