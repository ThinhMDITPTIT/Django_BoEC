from django.urls import path
from . import views

urlpatterns = [
    # Leave as empty string for base url
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login', views.loginForCustomer, name="login"),
    path('register', views.register, name="register"),
    path('customerprofile', views.customerprofile, name='customerprofile'),
    path('logout', views.logoutForCustomer, name='logout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('product/<int:pk>', views.detailproduct, name='detailproduct'),
    path('product/<str:name>', views.category, name='category'),
    path('product/<str:productname>', views.searchByName, name='searchByName'),
    path('add_comment/', views.addcomment, name='addcomment'),
    path('update_customer_inf/', views.updateEmail, name="update_customer_inf"),
    path('add_to_cart/', views.addtocart, name="addtocart"),
    path('cancel_order/', views.cancel_order, name="cancel_order"),
    path('staff/', views.staff_home, name="staff"),
    path('staff/<str:category>', views.category_order, name="categoryorder"),
    path('handler_order/', views.handler_order, name="handler_order")
]
