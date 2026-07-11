from django.urls import path, include
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('deals/', views.deals, name='deals'),
    path('customer-service/', views.customer_service, name='customer_service'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('set-location/', views.set_location, name='set_location'),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('accounts/', include('allauth.urls')),

    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<slug:product_slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/track/<int:order_id>/', views.track_package, name='track_package'),
    path('orders/return/<int:order_id>/', views.return_replace, name='return_replace'),

    # Profile & Backend
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
    

