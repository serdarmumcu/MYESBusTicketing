from django.shortcuts import render, redirect
from busticket.models import Bus,City,Driver,Trip,Reservation,BusCompany
from busticket.forms import BusForm,DriverForm,TripForm,ReservationForm,SearchForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import ProtectedError
from django.contrib.auth.models import User
from datetime import timedelta,datetime

# Create your views here.
def index(request):
    try:
        user = User.objects.get(username=request.user.username)
        if user.groups.name == 'BusCompany':
            return render(request,'busticket/home.html',{'company_name':user.buscompany})
        else:
            return render(request,'busticket/home.html',{'company_name':''})
    except:
        return HttpResponseRedirect("/login")

def busnew(request):  
    if request.method == "POST":  
        form = BusForm(request.POST)
        if form.is_valid():  
            try:  
                user = User.objects.get(username=request.user.username)
                form_result = form.save(commit=False)
                form_result.bus_company = user.buscompany
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
    user = User.objects.get(username=request.user.username)
    bus_list = Bus.objects.filter(bus_company=user.buscompany)
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
                user = User.objects.get(username=request.user.username)
                form_result = form.save(commit=False)
                form_result.bus_company = user.buscompany
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
    user = User.objects.get(username=request.user.username)
    driver_list = Driver.objects.filter(bus_company=user.buscompany)
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
    except ProtectedError as e:
        return JsonResponse( {"error":"Trip relation exists"} )
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )    
    return HttpResponseRedirect("/driver")    



def add_new_trip(request):  
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":  
        form = TripForm(user.buscompany,request.POST)  
        if form.is_valid():  
            try:  
                form_result = form.save(commit=False)
                form_result.bus_company = user.buscompany
                form.save()
                return HttpResponseRedirect("/trip")
            except:  
                pass
        else:
            print(form.errors)
    else:  
        form = TripForm(user.buscompany)  
    return render(request,'busticket/tripcrud/tripnew.html',{'form':form})  
def get_list_of_trips(request):  
    user = User.objects.get(username=request.user.username)
    trip_list = Trip.objects.filter(bus_company=user.buscompany)
    return render(request,"busticket/tripcrud/trip.html",{'trip_list':trip_list})  
def tripedit(request, id):  
    trip = Trip.objects.get(id=id)  
    user = User.objects.get(username=request.user.username)
    form = TripForm(user.buscompany,instance = trip)
    return render(request,'busticket/tripcrud/tripedit.html', {"form":form,"trip":trip})  
def update_trip_details(request, id):  
    trip = Trip.objects.get(id=id)  
    user = User.objects.get(username=request.user.username)
    form = TripForm(user.buscompany,request.POST, instance = trip)  
    if form.is_valid():  
        form.save()  
        return HttpResponseRedirect("/trip")
    else:
        print(form.errors)
    return render(request, 'busticket/tripcrud/tripedit.html', {'trip': trip})  
def delete_trip(request, id):  
    trip = Trip.objects.get(id=id)  
    try:
        trip.delete()  
    except ProtectedError as e:
        return JsonResponse( {"error":"Reservation relation exists"} )
    return HttpResponseRedirect("/trip")        

def search_trip(request):  
    now = datetime.now()
    trip = Trip.objects.filter(trip_date__gte=now.date())
    form = SearchForm()  
    return render(request,'busticket/searchtrip.html',{'trip_list': trip,'form':form}) 

def search(request):  
    form = SearchForm(request.POST)  
    if form.is_valid():
        from_city = form.cleaned_data["from_city"]   
        to_city = form.cleaned_data["to_city"]   
        bus_company = form.cleaned_data["bus_company"] 
        date_choice = form.cleaned_data["date_choice"] 
        now = datetime.now()
        lte_value = datetime.max
        kwargs = {}
        if from_city:
            city_f = City.objects.get(name=from_city)
            kwargs['from_city'] = city_f
        if to_city:
            city_t = City.objects.get(name=to_city)
            kwargs['to_city'] = city_t
        if bus_company:
            bus_c = BusCompany.objects.get(name=bus_company)
            kwargs['bus_company'] = bus_c
        if date_choice:
            if date_choice == 'Today':
                time_added = timedelta(hours = 24)               
            elif date_choice == 'This Week':
                days_per_week = 7
                time_added = timedelta(days = (days_per_week))
            elif date_choice == 'This Month':
                days_per_month = 30
                time_added = timedelta(days = (days_per_month))
            else:
                days_per_year = 365.24
                time_added = timedelta(days = (days_per_year))
                pass
            lte_value = now + time_added
        
        trip = Trip.objects.filter(**kwargs,trip_date__gte=now.date(),trip_date__lte=lte_value)
        return render(request,'busticket/searchtrip.html',{'trip_list': trip,'form':form}) 


def reservationnew(request, id):  
    trip = Trip.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":  
        form = ReservationForm(trip,user.passenger,True,request.POST)  
        if form.is_valid():  
            try:  
                user = User.objects.get(username=request.user.username)
                form_result = form.save(commit=False)
                now = datetime.now()
                hours_added = timedelta(hours = 3)
                now = now + hours_added
                form_result.reservation_date = now
                form.save()
                return HttpResponseRedirect("/reservation")
            except:  
                pass
        else:
            print(form.errors)
    else:  
        form = ReservationForm(trip,user.passenger,False)  
    return render(request,'busticket/reservationcrud/reservationnew.html',{'form':form,'trip':trip})  
def reservation(request):  
    user = User.objects.get(username=request.user.username)
    reservation_list = Reservation.objects.filter(passenger=user.passenger,is_ticket=False)
    return render(request,"busticket/reservationcrud/reservation.html",{'reservation_list':reservation_list})  
def reservationedit(request, id):  
    reservation = Reservation.objects.get(id=id) 
    user = User.objects.get(username=request.user.username) 
    form = ReservationForm(reservation.trip,user.passenger,False,instance = reservation)
    return render(request,'busticket/reservationcrud/reservationedit.html', {"form":form,"reservation":reservation})  
def reservationupdate(request, id):  
    reservation = Reservation.objects.get(id=id)  
    user = User.objects.get(username=request.user.username)
    form = ReservationForm(reservation.trip,user.passenger,False,request.POST, instance = reservation)  
    if form.is_valid():  
        form.save()  
        return HttpResponseRedirect("/reservation")
    else:
        print(form.errors)
    return render(request, 'busticket/reservationcrud/reservationedit.html', {"form":form, 'reservation': reservation})  
def reservationdelete(request, id):  
    reservation = Reservation.objects.get(id=id)  
    try:
        reservation.delete()
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )    
    return HttpResponseRedirect("/reservation")    

def purchaseticket(request, id):  
    reservation = Reservation.objects.get(id=id)  
    try:
        reservation.is_ticket = True
        reservation.save()
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )    
    return HttpResponseRedirect("/reservation")    

def ticket(request):  
    user = User.objects.get(username=request.user.username)
    ticket_list = Reservation.objects.filter(passenger=user.passenger,is_ticket=True)
    return render(request,"busticket/ticket.html",{'ticket_list':ticket_list})  