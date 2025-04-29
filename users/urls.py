from django.contrib import admin
from django.urls import path
from . import views as userViews,product_views


urlpatterns = [
    path('users', userViews.UserRegistrationView.as_view()),
    path('users/login', userViews.UsersLogin.as_view()),
    path('users/update/list/delete/<id>',userViews.UsersUpdateListDelete.as_view()),
    path('category', product_views.CategoryCreation.as_view()),
    path('products', product_views.ProductCreation.as_view()),
    path('products/update/list/delete/<id>', product_views.ProductUpdateViewDeleyeById.as_view()),
    path('products/search/', product_views.ProductSearchView.as_view()),
    path('add/to/cart', product_views.AddToCart.as_view()),
    path('add/to/cart/delete/list/<id>', product_views.AddToCartListDelete.as_view()),
    path('create/order/payment', product_views.CreateOrderAndPayment.as_view()),
    path('test', userViews.Test.as_view()),
]