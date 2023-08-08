from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout

from authentication.models import Pricing_Module, Week_Table ,TMF


# Create your views here.
def home(request):
    return render(request ,"authentication/index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST["username"]
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

 

        if User.objects.filter(username=username):
            messages.error(request , "Username already exist ! Please try some other username")
            return redirect(home)
        if User.objects.filter(email=email):
            messages.error(request ,"Email already exist " )
            return redirect(home)

        if pass1 != pass2:
            messages.error(request , "Passswords do not match , Please check the passowrd and try again")
            return redirect('home')

        if not username.isalnum():
            messages.error(request , "Username must be alpha numeric")
            return redirect(home)

        myuser = User.objects.create_user(username , email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request , "Your account has been succesfully created")
        return redirect("signin")
    return render(request ,"authentication/signup.html")


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username ,password=pass1)
        global x
        x = user.first_name
        if user is not None:
            login(request,user)
            fname = user.first_name
            
            return render(request , "authentication/index.html" ,{'fname':fname})

        else:
            messages.error(request ,"Bad Credentials!")
    return render(request ,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect('home')
    
def dashboard(request):
    query_results = Pricing_Module.objects.all()
    fullobj={}
    for item in query_results:
        objdict={
            "mod_id":item.mod_id,
            "dbp_price":item.dbp_price,
            "dbp_km":item.dbp_km,
            "dap":item.dap,
            "waiting_time":item.waiting_time,
            "waiting_charge":item.waiting_charge,
            "status":item.status,
            "usermodifiedby":item.usermodifiedby
    }
        days = Week_Table.objects.filter(mod_id=item.mod_id)
        dayarray=[]
        for day in days:
            dayarray.append(day.weekday)
        objdict["weekdays"]=dayarray
        tmf = TMF.objects.filter(mod_id=item.mod_id)
        timearray =[]
        timedictionary={}
        for t in tmf:
            timedictionary={
                t.hour:t.factor,
            }
            timearray.append(timedictionary)
        objdict["TMF"] = timearray
        fullobj[f"{item.mod_id}"]=objdict
    
    return render(request , 'authentication/dashboard.html',{"fullobj":fullobj})

def addform(request):
    if request.method == "POST":
        new_instance = Pricing_Module()

        new_instance.dbp_price = request.POST['dbp_price']
        new_instance.dbp_km = request.POST['dbp_km']
        weekdays = request.POST.getlist('option')
        new_instance.dap = request.POST['dap']
        TMF_time = request.POST.getlist('time[]')
        TMF_factor = request.POST.getlist('factor[]')
        new_instance.waiting_time = request.POST['waiting_time']
        new_instance.waiting_charge = request.POST['waiting_charge']
        new_instance.status = False
        if request.user.is_authenticated:
            user = request.user
        new_instance.usermodifiedby = user.first_name
        new_instance.save()
        instances = []
        for day in weekdays:
            instances.append(Week_Table(mod_id = new_instance , weekday = day))
        Week_Table.objects.bulk_create(instances)

        secondinstances = []
        for item1,item2 in zip(TMF_time, TMF_factor):
            print(item1, item2)
            secondinstances.append(TMF(mod_id = new_instance, hour = item1, factor = item2))
        TMF.objects.bulk_create(secondinstances)
    return render(request , "authentication/addform.html")

def editform(request):
    return render 