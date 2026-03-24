from django.urls import path
from . import views

urlpatterns =[
    path('userdash/',views.userdash,name='userdash'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('userorder/',views.userorder,name='userorder'),
    path('viewcart/',views.viewcart,name='viewcart'),
    path('userpass/',views.userpass,name='userpass'),
    path('addtocart/<bid>',views.addtocart,name='addtocart'),
    path('removeitem/<id>',views.removeitem,name='removeitem'),
    path('updateitem/<id><operator>',views.updateitem,name='updateitem'),
     path('checkout/',views.checkout,name='checkout'),
    path('payment-success/',views.payment_success,name='payment_success'),


]