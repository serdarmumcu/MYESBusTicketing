from django.shortcuts import render, redirect
from busticket.models import Bus,City,Driver,Trip,Reservation,BusCompany,Passenger,Transaction
from busticket.forms import BusForm,DriverForm,TripForm,ReservationForm,SearchForm,RegisterForm,SearchReservationsTicketsForm,BusCompanyForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import ProtectedError
from django.contrib.auth.models import User,Group
from datetime import timedelta,datetime
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY


def index(request):
    try:
        user = User.objects.get(username=request.user.username)
        if user.groups.name == 'BusCompany':
            return render(request,'busticket/home.html',{'company_name':user.buscompany})
        else:
            return render(request,'busticket/home.html',{'user_name':user.username})
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
    return render(request, 'busticket/tripcrud/tripedit.html', {"form":form,'trip': trip})  
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


def make_reservation(request, id):  
    trip = Trip.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    reservation_list = Reservation.objects.filter(trip = trip)
    ticket_list = Reservation.objects.filter(trip = trip,is_ticket=True)
    reservation_ids = []
    ticket_ids = []
    for item in reservation_list:
        reservation_ids.append(item.seat_no)
    for ticket in ticket_list:
        ticket_ids.append(ticket.seat_no)
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
    return render(request,'busticket/reservationcrud/reservationnew.html',{'form':form,'trip':trip, "numbers": range(1,trip.bus.seat_count + 1), "reservation_ids": reservation_ids, "ticket_ids": ticket_ids})  
def get_list_of_reservations(request):  
    user = User.objects.get(username=request.user.username)
    reservation_list = Reservation.objects.filter(passenger=user.passenger,is_ticket=False)
    return render(request,"busticket/reservationcrud/reservation.html",{'reservation_list':reservation_list})  
def update_reservation_details(request, id):  
    reservation = Reservation.objects.get(id=id) 
    user = User.objects.get(username=request.user.username) 
    form = ReservationForm(reservation.trip,user.passenger,False,instance = reservation)
    reservation_list = Reservation.objects.filter(trip = reservation.trip)
    ticket_list = Reservation.objects.filter(trip = reservation.trip,is_ticket=True)
    reservation_ids = []
    ticket_ids = []
    for item in reservation_list:
        reservation_ids.append(item.seat_no)
    for ticket in ticket_list:
        ticket_ids.append(ticket.seat_no)
    return render(request,'busticket/reservationcrud/reservationedit.html', {"form":form,"reservation":reservation, "numbers": range(1,reservation.trip.bus.seat_count + 1), "reservation_ids": reservation_ids, "ticket_ids": ticket_ids})  
def update_reservation(request, id):  
    reservation = Reservation.objects.get(id=id)  
    user = User.objects.get(username=request.user.username)
    form = ReservationForm(reservation.trip,user.passenger,False,request.POST, instance = reservation)  
    reservation_list = Reservation.objects.filter(trip = reservation.trip)
    ticket_list = Reservation.objects.filter(trip = reservation.trip,is_ticket=True)
    reservation_ids = []
    ticket_ids = []
    for item in reservation_list:
        reservation_ids.append(item.seat_no)
    for ticket in ticket_list:
        ticket_ids.append(ticket.seat_no)
    if form.is_valid():  
        form.save()  
        return HttpResponseRedirect("/reservation")
    else:
        print(form.errors)
    return render(request, 'busticket/reservationcrud/reservationedit.html', {"form":form, 'reservation': reservation, "numbers": range(1,reservation.trip.bus.seat_count + 1), "reservation_ids": reservation_ids, "ticket_ids": ticket_ids})  
def delete_reservation(request, id):  
    reservation = Reservation.objects.get(id=id)  
    try:
        reservation.delete()
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )    
    return HttpResponseRedirect("/reservation")    

def thanks(request,id):
    session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    reservation = Reservation.objects.get(id=id)  
    reservation.is_ticket = True
    now = datetime.now()
    hours_added = timedelta(hours = 3)
    now = now + hours_added
    amount = session["amount_total"]
    payment_intent = session["payment_intent"]
    t = Transaction.objects.create(transaction_date=now,charged_value=amount/100,payment_intent=payment_intent)
    reservation.transaction = t
    reservation.save()
    return HttpResponseRedirect("/ticket")      

def openpurchasepage(request, id):  
    reservation = Reservation.objects.get(id=id)  
    return render(request,'busticket/payment.html', {"reservation":reservation})

@csrf_exempt
def checkout(request, id):
    reservation = Reservation.objects.get(id=id) 
    price = int(reservation.trip.price * 100)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                'name': 'Bus Ticket',
                },
                'unit_amount': price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks', kwargs={'id': reservation.id})) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('openpurchasepage', kwargs={'id': id})),
    )

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    })

def ticket(request):  
    user = User.objects.get(username=request.user.username)
    ticket_list = Reservation.objects.filter(passenger=user.passenger,is_ticket=True)
    return render(request,"busticket/ticket.html",{'ticket_list':ticket_list})  

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            form.save()
            Passenger.objects.create(user=form.instance,name=name)
            g = Group.objects.get(name='Passenger')
            u = form.instance
            g.user_set.add(u)
            return redirect("/")
    else:
	    form = RegisterForm()
    return render(response, "registration/registration.html", {"form":form})

def search_reservationsandtickets(request):  
    user = User.objects.get(username=request.user.username)
    reservation = Reservation.objects.filter(trip__bus_company=user.buscompany)
    form = SearchReservationsTicketsForm(user.buscompany)
    return render(request,'busticket/reservationsandtickets.html',{'ticket_list': reservation,'form':form}) 

def reservationsandtickets(request):  
    user = User.objects.get(username=request.user.username)
    form = SearchReservationsTicketsForm(user.buscompany,request.POST)  
    if form.is_valid():
        trip = form.cleaned_data["trip"]      
        ticket_choice = form.cleaned_data["is_ticket"]
        kwargs = {}
        if trip:
            kwargs['trip'] = trip
        if ticket_choice == 'Ticket':
            kwargs['is_ticket'] = True
        elif ticket_choice == 'Reservation':
            kwargs['is_ticket'] = False

        reservation = Reservation.objects.filter(**kwargs,trip__bus_company=user.buscompany)
        return render(request,'busticket/reservationsandtickets.html',{'ticket_list': reservation,'form':form})

def buscompanyusernew(request):  
    if request.method == "POST":  
        form = BusCompanyForm(None,request.POST)
        if form.is_valid():  
            try:  
                name = form.cleaned_data.get('company_name')
                tel_no = form.cleaned_data.get('tel_no')
                address = form.cleaned_data.get('address')
                company_email = form.cleaned_data.get('company_email')
                url = form.cleaned_data.get('url')
                form.save()
                BusCompany.objects.create(user=form.instance,name=name,address=address,tel_no=tel_no,url=url,email=company_email)
                g = Group.objects.get(name='BusCompany')
                u = form.instance
                g.user_set.add(u)
                return HttpResponseRedirect("/buscompanyuser")
            except:  
                pass
        else:
            print(form.errors)
    else:  
        form = BusCompanyForm(None)  
    return render(request,'busticket/buscompanyusercrud/buscompanyusernew.html',{'form':form})  
def buscompanyuser(request):  
    buscompany_list = BusCompany.objects.filter()
    return render(request,"busticket/buscompanyusercrud/buscompanyuser.html",{'buscompany_list':buscompany_list})  
def buscompanyuseredit(request, id):  
    bus_company = BusCompany.objects.get(id=id)  
    form = BusCompanyForm(bus_company,instance = bus_company.user)
    return render(request,'busticket/buscompanyusercrud/buscompanyuseredit.html', {"form":form,"bus_company":bus_company})  
def buscompanyuserupdate(request, id):  
    bus_company = BusCompany.objects.get(id=id)  
    form = BusCompanyForm(bus_company,request.POST, instance = bus_company.user)  
    if form.is_valid():  
        name = form.cleaned_data.get('company_name')
        tel_no = form.cleaned_data.get('tel_no')
        address = form.cleaned_data.get('address')
        company_email = form.cleaned_data.get('company_email')
        url = form.cleaned_data.get('url')
        form.save()
        bus_company.name = name
        bus_company.tel_no = tel_no
        bus_company.address = address
        bus_company.email = company_email
        bus_company.url = url
        bus_company.save()
        return HttpResponseRedirect("/buscompanyuser")
    else:
        print(form.errors)
    return render(request, 'busticket/buscompanyusercrud/buscompanyuseredit.html', {'bus_company': bus_company})  
def buscompanyuserdelete(request, id):  
    bus_company = BusCompany.objects.get(id=id)  
    user = bus_company.user
    try:
        user.delete()
        bus_company.delete()
    except ProtectedError as e:
        return JsonResponse( {"error":"A relation exists"} )
    except Exception as e:
        return JsonResponse( {"error":"something went wrong"} )
    
    return HttpResponseRedirect("/buscompanyuser")

