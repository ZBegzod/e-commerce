from django.urls import path

from product.views import *

urlpatterns = [
    path('', product_list, name='list-product'),
    path('create-order/<int:product_id>/', CreateOrderView.as_view(), name='create-order'),
]
