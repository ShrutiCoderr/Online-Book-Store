from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from adminapp.models import*
from .models import*


# payment
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY



# Create your views here.
def userdash(request):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user':user
    }
    return render(request,"userdash.html",context)

def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request,"You are logged out successfully")
        return redirect('index')
    else:
            messages.warning(request,"something wents wrong.")
            return redirect('index')

def userprofile(request):
    if not 'userid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user':user
    }
    return render(request,"userprofile.html",context)
def editprofile(request):
    if not 'userid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user':user
    }
    if request.method == "POST":
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        picture = request.FILES.get('profile')
        address = request.POST.get('address')
        user.name = name
        user.contactno = contactno
        user.address = address
        if picture:
            user.picture = picture
        user.save()
        messages.success(request,"Your profile has been updated.")
        return redirect('userprofile')
    return render(request,"editprofile.html",context)
def userorder(request):
    if not 'userid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    orders = Order.objects.filter(user=user).order_by('ordered_at')
    orderitems =[]
    for order in orders:
        orderitems.append(OrderItem.objects.filter(order=order))
    context = {
        'userid':userid,
        'user':user,
        'order':orders,
        'orderitems':orderitems
    }
    return render(request,"userorder.html",context)
def viewcart(request):
    if not 'userid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart:
        Cart.objects.create(user=user)
    cart =Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)
    total_price =0
    for i in items:
        total_price += i.get_total_price()
    context = {
        'userid':userid,
        'user':user,
        'items':items,
        'total_price': total_price
    }
    return render(request,"viewcart.html",context)
def userpass(request):
    if not 'userid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    context = {
        'userid':userid,
        'user':user
    }
    return render(request,"userpass.html",context)

def addtocart(request,bid):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ucart = Cart.objects.filter(user=user)
    if not ucart:
        Cart.objects.create(user=user)
    cart =Cart.objects.get(user=user)
    book =Book.objects.get(id=bid)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity') or 1)
        ci = CartItem.objects.filter(cart=cart, book=book)
        if ci:
            item = CartItem.objects.get(cart=cart, book=book)
            item.quantity += quantity
            item.save()
        else:
            CartItem.objects.create(cart=cart, book=book, quantity=quantity)
        messages.success(request,f"{book.title} is added to cart")
        return redirect('index')
    else:
        messages.error(request,"Somethiing went wrong")
        return redirect('index')


def removeitem(request,id):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ci = CartItem.objects.filter(id=id)
    ci.delete()
    messages.success(request,"remove item from cart")
    return redirect('viewcart')


def updateitem(request,id,operator):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in ")
        return redirect('login')
    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    ci = CartItem.objects.get(id=id)
    if operator == "+":
        ci.quantity += 1
        if ci.book.stock < ci.quantity:
            messages.warning(request,"Item quantity is exceeded than stock")
            return redirect('viewcart')
    elif operator == "-":
        ci.quantity -= 1
        if ci.quantity == 0:
            ci.delete()
            messages.warning(request,"Removed")
            return redirect('viewcart')
    ci.save()
    messages.success(request,"Item quantity updated successfully")
    return redirect('viewcart')

def checkout(request):
    if 'userid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    if not settings.STRIPE_SECRET_KEY or settings.STRIPE_SECRET_KEY.startswith('sk_test_your'):
        messages.error(request, "Payment is not configured. Please set STRIPE_SECRET_KEY in your .env file.")
        return redirect('viewcart')

    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('viewcart')

    line_items = []

    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item.book.price * 100),
                'product_data': {
                    'name': item.book.title,
                },
            },
            'quantity': item.quantity,
        })

    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/userapp/payment-success/'),
            cancel_url=request.build_absolute_uri('/userapp/viewcart/'),
        )
        return redirect(session.url, code=303)
    except stripe.error.AuthenticationError:
        messages.error(request, "Payment configuration error. Please check your Stripe API key.")
        return redirect('viewcart')
    except Exception as e:
        messages.error(request, f"Payment error: {str(e)}")
        return redirect('viewcart')


def payment_success(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login')

    userid=request.session.get('userid')
    user = UserInfo.objects.get(email=userid)

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect('index')

  
        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
            book = Book.objects.get(id = item.book.id)
            book.stock = book.stock - item.quantity
            book.save()

        cart_items.delete()

        items = OrderItem.objects.filter(order=order)

        # Add total_price attribute to each item
        for item in items:
            item.total_price = item.quantity * item.price

        
        messages.success(request, "Payment successful! Your order has been placed.")
        return render(request, 'payment_success.html', {'order': order})

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('index')






