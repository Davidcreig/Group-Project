from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from helloworld.forms import loginForm, bookingForm ,signUpForm
from django.contrib.auth.models import User
from helloworld.models import Equipment, Booking
# Create your views here.

def UserLoggedIn(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def GetUserName(request):
    return request.user.username
    
def authBooking(bookingDetails):
    canBook = True
    if Equipment.objects.filter(id = bookingDetails['itemID']).exists() and User.objects.filter(id = bookingDetails['accountID']).exists():
        if Booking.objects.filter(startDate = bookingDetails['itemID']).exists:
            for i in Booking.objects.filter(startDate = bookingDetails['itemID']):
                if ((i.startDate <= bookingDetails['endDate'] <= i.endDate) and (i.startDate <= bookingDetails['startDate'] <= i.endDate)):
                    canBook = False
        else:
            canBook = False
        return canBook
    else:
        return False


def home(request):

    return render(request,"home.html")

def account(request):
    if UserLoggedIn(request) == True:
        context = {
        'username':GetUserName(request)
        }
        return render(request,"account.html",context)
    else:
        return render(request,"login.html")

def bookingPage(request):

    return render(request,"booking.html")

def signUp(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        # create a form instance and populate it with data from the request:
        form = signUpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                context = {
                'form':form,
                'user':user
                }
        # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {
                'form':form
                }
                return render(request,"signup.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = signUpForm()
        context = {
        'form':form
        }

        return render(request,"signup.html",context) 
    return render(request,"signup.html")

def loginPage(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # create a form instance and populate it with data from the request:
        form = loginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                context = {
                'form':form,
                'user':user
                }
        # Redirect to a success page.
                return render(request,"home.html",context)
            else:
                context = {
                'form':form
                }
                return render(request,"login.html", context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = loginForm()
        context = {
        'form':form
        }

        return render(request,"login.html",context) 
    

def accountPage(request):
    return render(request,"account.html")

def userLogout(request):
        logout(request)
        return render(request,"home.html")

def bookingPage(request):
    equipment = Equipment.objects.all()

    if request.method == "POST":
        form = bookingForm(request.POST)
        if form.is_valid():
            accountID = request.POST["accountID"]
            itemID = request.POST["itemID"]
            startDate = request.POST["startDate"]
            endDate = request.POST["endDate"]
            bookingStatus = True
            context = {
            'equipment':equipment,
            'accountID':accountID,
            'itemID':itemID,
            'startDate':startDate,
            'endDate':endDate,
            'bookingStatus':bookingStatus
            }
            context['bookingStatus'] = authBooking(context)
            if context['bookingStatus'] == True:
            #Do some stuff to save to DB
        
                return render(request,"booking.html",context)
    form = bookingForm()
    context = {
        'equipment':equipment,
        'accountID':1,
        'itemID':1,
        'startDate':1,
        'endDate':1,
        'bookingStatus':False
        }
    return render(request,"booking.html", context)