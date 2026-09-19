from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('addtocart',views.addtocart,name="addtocart"),
    path('cart',views.cart,name="cart"),
    path('fav',views.fav,name="fav"),
    path('favview',views.favview,name="favview"),
    path('remove_cart/<int:cid>',views.remove_cart,name="remove_cart"),
    path('remove_fav/<int:fid>',views.remove_fav,name="remove_fav"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.product_details,name="product_details"),
]