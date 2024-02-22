from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.home,name='home'),
    path('register/',views.registerpage,name='register'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('user/',views.userpage,name='user-page'),
    path('account/',views.accountsettings,name='account'),
    path('product/',views.products,name='products'),
    path('customer/<str:pk>/',views.customers,name='customers'),
    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    

]