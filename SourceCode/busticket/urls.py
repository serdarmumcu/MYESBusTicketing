from django.urls import path
from busticket import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bus/',views.bus),  
    path('busnew/',views.busnew),  
    path('busedit/<int:id>', views.busedit),  
    path('busupdate/<int:id>', views.busupdate),  
    path('busdelete/<int:id>', views.busdelete),  
    # path('bus/', views.bus, name='bus'),
    # path('createbus/', views.createbus, name='createbus'),
    # path('driver/', views.driver, name='driver'),
    # path('trip/', views.trip, name='trip'),
]
