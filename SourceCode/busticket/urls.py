from django.urls import path
from busticket import views

urlpatterns = [
    path('', views.index, name='index'),
]
