from django.urls import path
from core import views


urlpatterns = [
   path('', views.index, name='index'),
   path('add_product/', views.add_product, name='add_product'),
   path('product_desc/<pk>', views.product_desc, name='product_desc'),
   path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
   path('order_list/', views.order_list, name='order_list'),
   path('add_item/<int:pk>', views.add_item, name='add_item'),
   path('remove_item/<int:pk>', views.remove_item, name='remove_item'),
   path('checkout/', views.checkout_page, name='checkout_page'),
]