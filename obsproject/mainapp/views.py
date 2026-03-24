from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from adminapp.models import*
# Create your views here.

def index(request):
    userid = request.session.get('userid')
    books = Book.objects.all()
    context ={
        'books': books,
        'userid':userid
    }
    return render(request, "index.html",context)

def about(request):
    userid = request.session.get('userid')
    context = {
        'userid' : userid
    }
    return render(request, "about.html",context)

def contact(request):
    userid = request.session.get('userid')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Enquiry.objects.create(name=name,email=email,contactno=contactno,subject=subject,message=message)
        messages.success(request,"Enguiry has been submitted successfully.")
        return redirect('contact')
    context = {
        'userid': userid
    }
    return render(request, "contact.html",context)

def login(request):
    userid = request.session.get('userid')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(usertype="user", username=username,password=password)
            if user is not None:
                messages.success(request,"Welcome user")
                request.session['userid'] = user.username
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, "login.html")


def register(request):
    userid = request.session.get('userid')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        password = request.POST.get('password')
        cpasssword = request.POST.get('cpassword')
        if password != cpasssword:
            messages.warning(request,"Invalid Password")
            return redirect('register')
        check = LoginInfo.objects.filter(username=email)
        if check:
            messages.warning(request,"This email is already registered.")
        log = LoginInfo(username=email,password=password)
        user = UserInfo(login=log,name=name,email=email,contactno=contactno)
        log.save()
        user.save()
        messages.success(request,"Registration successfully")
        return redirect('register')
    context ={
            'userid': userid
        }
    return render(request, "register.html",context)

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            admin = LoginInfo.objects.get(usertype="admin", username=username,password=password)
            if admin is not None:
                messages.success(request,"Welcome Admin")
                request.session['adminid'] = admin.username
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid credentials")
            return redirect('adminlogin')
    return render(request,"adminlogin.html")

def book_details(request,id):
    book=Book.objects.get(id=id)
    context ={
        'book':book,
    }
    return render(request,"book_details.html",context)

