from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from shop import views 

urlpatterns=[
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:c_name>/<str:p_name>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('cart',views.cart_page,name="cart"),
    path('removecart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('premium',views.premium,name='premium'),
   
]
