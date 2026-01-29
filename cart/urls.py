from cart import views as cart_views
from shop import views as shop_views
from django.urls import path
from django.contrib.auth.views import LogoutView
app_name = 'cart'
urlpatterns = [
    path("<int:i>/", cart_views.AddToCart.as_view(), name='addtocart'),
    path("cartview/", cart_views.CartDetail.as_view(), name='cartdetail'),
    path('about/<int:id>/', shop_views.AboutView.as_view(), name='about'),
    path('cartdecrement/<int:id>/', cart_views.Cartdecrement.as_view(), name='cartdecrement'),
    path('cartdelete/<int:id>/', cart_views.Cartdelete.as_view(), name='cartdelete'),
    path('checkout/', cart_views.CheckoutView.as_view(), name='checkout'),
    path('success/<i>/', cart_views.paymentsuccess.as_view(), name='success'),
    path('orders/', cart_views.Ordersummary.as_view(), name='orders'),
]

