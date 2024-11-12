from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('ordersuccess/',views.ordersuccess,name='ordersuccess'),
    path('productdetails/<int:id>',views.productdetails,name='productdetails'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('verify/<slug:id>',views.verify1,name='verify'),
    path('deleteFromcart/<int:id>',views.deleteFromcart,name='deleteFromcart'),
    path('blocked/',views.blocked,name='blocked'),
    path('vieworders/',views.vieworders,name='vieworders'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('unblockrequests/',views.unblockrequests,name='unblockrequests'),
    path('updatestatus/<int:id>',views.updatestatus,name='updatestatus'),
    path('unblock/<int:id>',views.unblock,name='unblock'),
]
