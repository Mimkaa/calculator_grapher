from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView,ListView
from .models import Buss_Schedule,Sit,Book
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
def Initial(request):
    return render(request,'initial.html',{})


def HomeView(request):
    object_list=Buss_Schedule.objects.all()
    user=request.user
    books=user.book_set.all()



# sits=user.sit_set.all()
#     trips=Buss_Schedule.objects.all()
#     for trip in trips:
#         if not trip.book_set.exists():
#             sits=trip.sit_set.all()
#             for sit in sits:
#                 if sit.booking.filter(id=request.user.id).exists():
#                     sit.booking.remove(request.user)

    sits=user.sit_set.all()
    if not user.book_set.exists():

        for sit in sits:

            if sit.booking.filter(id=request.user.id).exists():
                sit.booking.remove(request.user)



    return render(request,"home.html",{'object_list':object_list,"sits":sits,'books':books})

class DetailTripView(DetailView):
    model = Buss_Schedule
    template_name = 'trip_details.html'

class AddTripView(CreateView):
    model = Buss_Schedule
    template_name = 'create_trip.html'
    fields=('bus_pic','dest_pic','destination','departure','trip_duration','trip_distance','author')

class DeleteTripView(DeleteView):
    model = Buss_Schedule
    template_name = 'delete_trip.html'
    success_url=reverse_lazy("home")

class UpdateTripView(UpdateView):
    model = Buss_Schedule
    template_name = 'edit_trip.html'
    success_url = reverse_lazy("home")
    fields = '__all__'

class CreateSitView(CreateView):
    model=Sit
    template_name = 'create_sit.html'
    success_url = reverse_lazy('home')
    fields = ('number','schedule')
    def get_success_url(self, *args, **kwargs):
        #return HttpResponseRedirect(reverse("article_details",args=[str(self.kwargs['pk'])]))

        return reverse("trip_details",args=[str(self.kwargs['pk'])])

def EditSitsView(request,pk):
    trip=get_object_or_404(Buss_Schedule, id=pk)
    booked1=False


    if trip.sit_set.filter(number='1').exists() and trip.sit_set.get(number='1').booking.exists():
            booked1=True

    booked2=False
    if trip.sit_set.filter(number='2').exists() and trip.sit_set.get(number='2').booking.exists():
            booked2=True

    booked3=False
    if trip.sit_set.filter(number='3').exists() and trip.sit_set.get(number='3').booking.exists():
            booked3=True

    booked4=False
    if trip.sit_set.filter(number='4').exists() and trip.sit_set.get(number='4').booking.exists():
            booked4=True

    booked5=False
    if trip.sit_set.filter(number='5').exists() and trip.sit_set.get(number='5').booking.exists():
            booked5=True

    booked6=False
    if trip.sit_set.filter(number='6').exists() and trip.sit_set.get(number='6').booking.exists():
            booked6=True

    booked7=False
    if trip.sit_set.filter(number='7').exists() and trip.sit_set.get(number='7').booking.exists():
            booked7=True

    booked8=False
    if trip.sit_set.filter(number='8').exists() and trip.sit_set.get(number='8').booking.exists():
            booked8=True

    booked9=False
    if trip.sit_set.filter(number='9').exists() and trip.sit_set.get(number='9').booking.exists():
            booked9=True

    booked10=False
    if trip.sit_set.filter(number='10').exists() and trip.sit_set.get(number='10').booking.exists():
            booked10=True

    booked11=False
    if trip.sit_set.filter(number='11').exists() and trip.sit_set.get(number='11').booking.exists():
            booked11=True

    booked12=False
    if trip.sit_set.filter(number='12').exists() and trip.sit_set.get(number='12').booking.exists():
            booked12=True

    booked13=False
    if trip.sit_set.filter(number='13').exists()and trip.sit_set.get(number='13').booking.exists():
            booked13=True

    booked14=False
    if trip.sit_set.filter(number='14').exists() and trip.sit_set.get(number='14').booking.exists():
            booked14=True

    booked15=False
    if trip.sit_set.filter(number='15').exists() and trip.sit_set.get(number='15').booking.exists():
            booked15=True

    booked16=False
    if trip.sit_set.filter(number='16').exists() and trip.sit_set.get(number='16').booking.exists():
            booked16=True

    booked17=False
    if trip.sit_set.filter(number='17').exists() and trip.sit_set.get(number='17').booking.exists():
            booked17=True

    booked18=False
    if trip.sit_set.filter(number='18').exists()and trip.sit_set.get(number='18').booking.exists():
            booked18=True

    booked19=False
    if trip.sit_set.filter(number='19').exists() and trip.sit_set.get(number='19').booking.exists():
            booked19=True

    booked20=False
    if trip.sit_set.filter(number='20').exists() and trip.sit_set.get(number='20').booking.exists():
            booked20=True

    booked21=False
    if trip.sit_set.filter(number='21').exists() and trip.sit_set.get(number='21').booking.exists():
            booked21=True

    booked22=False
    if trip.sit_set.filter(number='22').exists() and trip.sit_set.get(number='22').booking.exists():
            booked22=True

    booked23=False
    if trip.sit_set.filter(number='23').exists() and trip.sit_set.get(number='23').booking.exists():
            booked23=True

    booked24=False
    if trip.sit_set.filter(number='24').exists() and trip.sit_set.get(number='24').booking.exists() :
            booked24=True

    user=request.user


    sits=user.sit_set.all()
    sits=[obj for obj in sits if trip.sit_set.filter(id=obj.id).exists()]
    objects=len(sits)
    price=0
    if request.user.status=='AD':
        price=objects*10
    if request.user.status=='SD':
        price=objects*7
    if request.user.status=='SC':
        price=objects*3

    #remove book in it is empty
    books=Book.objects.all()
    check_list=[]
    for book in books:
            for sit in   book.trip.sit_set.all():
                if sit.booking.filter(id=request.user.id).exists():
                    check_list.append(1)
            if len(check_list)==0: #and check_list.count(check_list[0])==len(check_list):
                Book.objects.all().get(id=book.id).delete()

    return render(request,'edit_sits.html',{'sits':sits,'price':price,"how_many_booked":objects,"booked1":booked1,'buss_schedule':trip,"booked2":booked2,"booked3":booked3,"booked4":booked4,"booked5":booked5,"booked6":booked6,"booked7":booked7,"booked8":booked8,"booked9":booked9,"booked10":booked10,"booked11":booked11,"booked12":booked12
        ,"booked13":booked13,"booked14":booked14,"booked15":booked15,"booked16":booked16,"booked17":booked17,"booked18":booked18,"booked19":booked19,"booked20":booked20,"booked21":booked21,"booked22":booked22,"booked23":booked23,"booked24":booked24})

def BookView(request,pk):
    trip=get_object_or_404(Buss_Schedule, id=pk)
    sit=trip.sit_set.get(number=request.POST.get('sit_id'))
    if sit.booking.filter(id=request.user.id).exists():
        sit.booking.remove(request.user)
    elif not sit.booking.exists():

        sit.booking.add(request.user)



    return HttpResponseRedirect(reverse("edit_sits",args=[str(pk)]))

class ListOfSits(ListView):
    model = Sit
    template_name = 'list_of_sits.html'


class DeleteSitView(DeleteView):
    model = Sit
    template_name = 'delete_sit.html'
    def get_success_url(self, *args, **kwargs):
        #return HttpResponseRedirect(reverse("article_details",args=[str(self.kwargs['pk'])]))

        return reverse("list_of_sits",args=[str(self.kwargs['pk'])])

class DeleteBookView(DeleteView):
    model = Book
    template_name = 'delete_book.html'
    def get_success_url(self, *args, **kwargs):
        #return HttpResponseRedirect(reverse("article_details",args=[str(self.kwargs['pk'])]))

        return reverse("showorders")

def ThanksView(request):
    user=request.user

    books=user.book_set.all()

    return render(request,'thanks.html',{"books":books})

def CreateABookView(request,pk):
    user=request.user
    tripp=get_object_or_404(Buss_Schedule,id=pk)

    if not tripp.book_set.exists():
        book=Book()
        book.trip_id=tripp.id
        book.save()
        book.user.add(request.user)
        if user.sit_set.exists():
            for sit in user.sit_set.all():
                book.sits.add(sit)

        book.save()
    else:
        book=Book.objects.get(trip=tripp)




        if book.sits.exists():
            for sit in book.sits.all():
                book.sits.remove(sit)

        if user.sit_set.exists():
            for sit in user.sit_set.all():
                book.sits.add(sit)

    #remove book in it is empty
    books=Book.objects.all()
    check_list=[]
    for book in books:
            for sit in   book.trip.sit_set.all():
                if sit.booking.filter(id=request.user.id).exists():
                    check_list.append(1)
            if len(check_list)==0: #and check_list.count(check_list[0])==len(check_list):
                Book.objects.all().get(id=book.id).delete()

    return HttpResponseRedirect(reverse("thanks"))

def ShowAllOrdersView(request):
    user=request.user
    books=user.book_set.all()
    trip_sit={}
    list=[]



    for book in books:


        sits=book.trip.sit_set.all()
        list=[i for i in sits if i.booking.filter(id=request.user.id).exists()]
        trip_sit[book]=list




    #sits_count=book.sits.all().count()
    price=0

    if request.user.status=='AD':
        price=10
    if request.user.status=='SD':
        price=7
    if request.user.status=='SC':
        price=3

    return render(request,'ordered.html',{"price":price,"trip_sit":trip_sit})




