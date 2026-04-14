from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [

    # HOME
    path('', home, name='home'),

    # STATIC PAGES
    path('contact/', contact, name='contact'),
    

    #checkout page
    path('checkout/',checkout,name="checkout"),
    #login
    path('login/',user_login,name='user_login'),

    #log_out
    path('logout/',user_logout,name='user_logout'),

    #register
    path('register/',user_register,name='user_register'),

    # STORE (BASE)
    path('store/', store, name='store'),

    #do order
    path('do-order/',do_order,name="do_order"), 

    #password change based on old password
    path('change-password/',old_pass_change,name="old_pass_change"),

    #forget password urls
    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/pass/forgot_password.html'
        ),
        name='password_reset'
    ),

    path(
        'forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/pass/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/pass/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/pass/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    
    #profile
    path('profile/',profile,name="profile"),


    # STORE → CATEGORY
    path(
        'store/<slug:category_slug>/',
        store,
        name='store_by_category'
    ),

    # STORE → SUBCATEGORY
    path(
        'store/<slug:category_slug>/<slug:sub_slug>/',
        store,
        name='store_by_subcategory'
    ),

    # PRODUCT DETAIL (MOST SPECIFIC)
    path(
        '<slug:category_slug>/<slug:sub_slug>/<slug:brand_slug>/<slug:product_slug>/',
        product_detail,
        name='product_detail'
    ),

    # CART
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail, name='cart_detail'),
]
