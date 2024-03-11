from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('plat/<int:id>/', views.plat_detail, name='plat'),
    path('go-to-cart/', views.go_to_cart, name="go-to-cart"),
    path('plat/add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('delete-order/', views.delete_order, name='delete-order'),
    path('modify-order/', views.modify_order, name='modify-order'),
    path('pay-for-shopping/', views.pay_for_shopping, name='pay-for-shopping'),
]




    # path('plat/<int:id>/add-to-cart-from-menu/', views.add_to_cart_from_menu, name='add-to-cart-from-menu'),
    # path('plat/<int:id>/add-to-cart-from-more-details/', views.add_to_cart_from_more_details, name='add-to-cart-from-more-details'),

