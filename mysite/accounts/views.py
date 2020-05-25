from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from django.contrib import messages
from .models import surform
# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return redirect('login')
    else:
        return render(request,'login.html')
def home(request):
    return render(request,'login.html')
def register(request):
    if request.method =='POST':
        firstname=request.POST['first_name']
        username=request.POST['username']
        passw=request.POST['password']
        em=request.POST['email']
        user= User.objects.create_user(username=username,first_name=firstname,password=passw,email=em)
        user.save()
        return redirect('login')
    else:
        return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def survey(request):
    if request.method=='POST':
        name=request.POST['name']
        age=request.POST['age']
        s=surform(name=name,age=age)
        s.save()
        return redirect('/')
    else:
        return render(request,'survey.html')