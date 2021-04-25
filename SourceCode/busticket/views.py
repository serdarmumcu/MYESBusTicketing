from django.shortcuts import render, redirect
from busticket.models import Bus
from busticket.forms import BusForm
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request,'busticket/home.html',{})


def busnew(request):  
    if request.method == "POST":  
        form = BusForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass 
    else:  
        form = BusForm()  
    return render(request,'busticket/busnew.html',{'form':form})  
def bus(request):  
    bus_list = Bus.objects.all()
    return render(request,"busticket/bus.html",{'bus_list':bus_list})  
def busedit(request, id):  
    bus = Bus.objects.get(id=id)  
    return render(request,'busticket/busedit.html', {'bus':bus})  
def busupdate(request, id):  
    bus = Bus.objects.get(id=id)  
    form = BusForm(request.POST, instance = bus)  
    if form.is_valid():  
        form.save()  
        return redirect("/")  
    return render(request, 'busticket/busedit.html', {'bus': bus})  
def busdelete(request, id):  
    bus = Bus.objects.get(id=id)  
    bus.delete()  
    return redirect("/")  

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