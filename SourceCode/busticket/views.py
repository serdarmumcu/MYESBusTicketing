from django.shortcuts import render, redirect
from busticket.models import Bus,Driver,Trip
from busticket.forms import BusForm,DriverForm,TripForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import ProtectedError

# Create your views here.
def index(request):
    return render(request,'busticket/home.html',{})


def busnew(request):  
    if request.method == "POST":  
        form = BusForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return HttpResponseRedirect("/bus")
            except:  
                pass
        else:
            print(form.errors)
    else:  
        form = BusForm()  
    return render(request,'busticket/buscrud/busnew.html',{'form':form})  
def bus(request):  
    bus_list = Bus.objects.all()
    return render(request,"busticket/buscrud/bus.html",{'bus_list':bus_list})  
def busedit(request, id):  
    bus = Bus.objects.get(id=id)  
    form = BusForm(instance = bus)
    return render(request,'busticket/buscrud/busedit.html', {"form":form,"bus":bus})  
def busupdate(request, id):  
    bus = Bus.objects.get(id=id)  
    form = BusForm(request.POST, instance = bus)  
    if form.is_valid():  
        form.save()  
        return HttpResponseRedirect("/bus")
    else:
        print(form.errors)
    return render(request, 'busticket/buscrud/busedit.html', {'bus': bus})  
def busdelete(request, id):  
    bus = Bus.objects.get(id=id)  
    try:
        bus.delete()
        return JsonResponse( {"error":""} )
    except ProtectedError as e:
        return JsonResponse( {"error":"Trip relation exists"} )
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )
    
    return HttpResponseRedirect("/bus")



def drivernew(request):  
    if request.method == "POST":  
        form = DriverForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return HttpResponseRedirect("/driver")
            except:  
                pass
        else:
            print(form.errors)
    else:  
        form = DriverForm()  
    return render(request,'busticket/drivercrud/drivernew.html',{'form':form})  
def driver(request):  
    driver_list = Driver.objects.all()
    return render(request,"busticket/drivercrud/driver.html",{'driver_list':driver_list})  
def driveredit(request, id):  
    driver = Driver.objects.get(id=id)  
    form = DriverForm(instance = driver)
    return render(request,'busticket/drivercrud/driveredit.html', {"form":form,"driver":driver})  
def driverupdate(request, id):  
    driver = Driver.objects.get(id=id)  
    form = DriverForm(request.POST, instance = driver)  
    if form.is_valid():  
        form.save()  
        return HttpResponseRedirect("/driver")
    else:
        print(form.errors)
    return render(request, 'busticket/drivercrud/driveredit.html', {'driver': driver})  
def driverdelete(request, id):  
    driver = Driver.objects.get(id=id)  
    try:
        driver.delete()  
        return JsonResponse( {"error":""} )
    except ProtectedError as e:
        return JsonResponse( {"error":"Trip relation exists"} )
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )    
    return HttpResponseRedirect("/driver")    



def add_new_trip(request):  
    if request.method == "POST":  
        form = TripForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return HttpResponseRedirect("/trip")
            except:  
                pass
        else:
            print(form.errors)
    else:  
        form = TripForm()  
    return render(request,'busticket/tripcrud/tripnew.html',{'form':form})  
def get_list_of_trips(request):  
    trip_list = Trip.objects.all()
    return render(request,"busticket/tripcrud/trip.html",{'trip_list':trip_list})  
def update_trip_details(request, id):  
    trip = Trip.objects.get(id=id)  
    form = TripForm(instance = trip)
    return render(request,'busticket/tripcrud/tripedit.html', {"form":form,"trip":trip})  
def tripupdate(request, id):  
    trip = Trip.objects.get(id=id)  
    form = TripForm(request.POST, instance = trip)  
    if form.is_valid():  
        form.save()  
        return HttpResponseRedirect("/trip")
    else:
        print(form.errors)
    return render(request, 'busticket/tripcrud/tripedit.html', {'trip': trip})  
def delete_trip(request, id):  
    trip = Trip.objects.get(id=id)  
    trip.delete()  
    return HttpResponseRedirect("/trip")        

# def bus(request):
#     bus_list = Bus.objects.all()
#     return render(request,"bus.html",{'employees':bus_list}) 
    # if request.method == "POST":
    #     print(request.POST)
    #     if request.POST.get('save'):
    #         for item in bus_list:
    #             item.plate_text = request.POST.get(str(item.id))
    #             item.save()
    #     else:
    #         return HttpResponseRedirect("/createbus")

    # my_dict = {'bus_records': bus_list}
    # return render(request,'busticket/bus.html',context=my_dict)

# def driver(request):
#     bus_list = Bus.objects.all()

#     if request.method == "POST":
#         print(request.POST)
#         if request.POST.get('save'):
#             for item in bus_list:
#                 item.plate_text = request.POST.get(str(item.id))
#                 item.save()
#         else:
#             return HttpResponseRedirect("/createbus")

#     my_dict = {'bus_records': bus_list}
#     return render(request,'busticket/bus.html',context=my_dict)


# def trip(request):
#     bus_list = Bus.objects.all()

#     if request.method == "POST":
#         print(request.POST)
#         if request.POST.get('save'):
#             for item in bus_list:
#                 item.plate_text = request.POST.get(str(item.id))
#                 item.save()
#         else:
#             return HttpResponseRedirect("/createbus")

#     my_dict = {'bus_records': bus_list}
#     return render(request,'busticket/bus.html',context=my_dict)       


# def createbus(request):
#     if request.method == "POST":
#         form = CreateNewBus(request.POST)
#         if form.is_valid():
#             plate = form.cleaned_data["plate_text"]
#             brand = form.cleaned_data["brand_name"]
#             status = form.cleaned_data["status"]
#             b = Bus(plate_text=plate,brand_name=brand,status=status)
#             b.save()
#         #return HttpResponseRedirect("/%i" % t.id)
#         return HttpResponseRedirect("/bus")
#     else:
#         form = CreateNewBus()
#     return render(request,'busticket/createbus.html',{"form":form})