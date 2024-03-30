from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),

    path('product',views.product,name='product'),
    path('search/',views.search,name='search'),
    path('contact', views.contact, name='contact'),


#add to cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',  views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),

    path('cart/checkout/', views.checkout, name='checkout'),

path('cart/checkout/placeorder', views.place_order, name='place_order'),

]

