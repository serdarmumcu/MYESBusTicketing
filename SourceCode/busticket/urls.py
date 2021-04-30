from django.urls import path
from busticket import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bus/',views.bus),  
    path('busnew/',views.busnew),  
    path('busedit/<int:id>', views.busedit),  
    path('busupdate/<int:id>', views.busupdate),  
    path('busdelete/<int:id>', views.busdelete),  
    path('driver/',views.driver),  
    path('drivernew/',views.drivernew),  
    path('driveredit/<int:id>', views.driveredit),  
    path('driverupdate/<int:id>', views.driverupdate),  
    path('driverdelete/<int:id>', views.driverdelete), 
    path('trip/',views.get_list_of_trips),  
    path('tripnew/',views.add_new_trip),  
    path('tripedit/<int:id>', views.update_trip_details),  
    path('tripupdate/<int:id>', views.tripupdate),  
    path('tripdelete/<int:id>', views.delete_trip), 
    # path('bus/', views.bus, name='bus'),
    # path('createbus/', views.createbus, name='createbus'),
    # path('driver/', views.driver, name='driver'),
    # path('trip/', views.trip, name='trip'),
]
