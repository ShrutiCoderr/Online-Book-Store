from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from .models import*
from userapp.models import*

# Create your views here.
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    total_revenue = 0
    orders = Order.objects.all()
    for order in orders:
        total_revenue += order.total_amount 
    context = {
        'adminid' :  adminid,
        'user_count': UserInfo.objects.all().count(),
        'book_count': Book.objects.all().count(),
        'cat_count': Order.objects.all().count(),
        'order_count': Order.objects.all().count(),
        'enqs_count': Enquiry.objects.all().count(),
        'total_revenue': total_revenue
    }
    return render(request, "admindash.html",context)

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"You are Logged out.")
        return redirect('index')
    else:
        messages.error(request,'Somthing Went Wrong.')
        return redirect('index')
    
def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid' :  adminid
    }
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        check = Category.objects.filter(name=name)
        if check:
            messages.warning(request,"Category already exists.")
            return redirect('addcat')
        Category.objects.create(name=name,description=description)
        messages.success(request,"Category added successfully.")
        return redirect('addcat')

    return render(request, "addcat.html",context)

def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    cats=Category.objects.all()
    context = {
        'adminid' :  adminid,
        'cats': cats,
    }
    return render(request, "viewcat.html",context)

def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    categories = Category.objects.all()
    context = {
        'adminid' :  adminid,
        'categories': categories
    }
    if request.method == "POST":
        title = request.POST.get('title')
        author=request.POST.get('author')
        catid =request.POST.get('catid')
        cat=Category.objects.get(id=catid)
        # category=cat,
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price = request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        Book.objects.create(
            title=title,
            author=author,
            category=cat,
            description=description,
            original_price=original_price,
            price=price,
            published_date=published_date,
            language=language,
            cover_image=cover_image,
            stock=stock
        )
        messages.success(request,"New book added successfully")
        return redirect('addbook')
    return render(request, "addbook.html",context)

def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid' :  adminid
    }
    return render(request, "viewbook.html",context)

def viewenqs(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    enqs = Enquiry.objects.all()
    context = {
        'adminid' :  adminid,
        'enqs' : enqs,
    }
    return render(request, "viewenqs.html",context)

def adminpassword(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not Logged in.")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid' :  adminid
    }
    return render(request, "adminpassword.html",context)

