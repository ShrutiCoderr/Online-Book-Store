from django.urls import path
from .import views
urlpatterns = [
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout, name='adminlogout'),
    path('addcat/',views.addcat, name='addcat'),
    path('viewcat/',views.viewcat, name='viewcat'),    
    path('addbook/',views.addbook, name='addbook'),    
    path('viewbook/',views.viewbook, name='viewbook'),    
    path('viewenqs/',views.viewenqs, name='viewenqs'),    
    path('adminpassword/',views.adminpassword, name='adminpassword'),    


]