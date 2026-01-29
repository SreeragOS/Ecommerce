from search import views
from django.urls import path
from django.contrib.auth.views import LogoutView
app_name = 'search'
urlpatterns = [
    path("", views.SearchView.as_view(), name='search'),
    
]
