from shop import views
from django.urls import path
from django.contrib.auth.views import LogoutView
app_name = 'shop'
urlpatterns = [
    path("", views.categoryView.as_view(), name='categories'),
    path("product/<int:i>/", views.productView.as_view(), name='product'),
    path('about/<int:id>/', views.AboutView.as_view(), name='about'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='shop:categories'), name='logout'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-product/', views.add_product, name='add_product'),
]
