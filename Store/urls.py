from django.urls import path
from . import views as store


urlpatterns = [
    path('', store.home, name='home'),
    path('cart/', store.cart, name='cart'),
    path('checkout/', store.checkout, name='checkout'),
    path('products/<slug>/', store.productList, name='products'),
    path('product/<int:pk>/', store.ProductDetails.as_view(), name='details'),
    path('update_item/', store.updateItem, name="update_itme"),
    path('process_order/', store.processOrder, name="process_order"),
]
