from django.shortcuts import render, redirect
from django.views import View
from shop.models import Category as categories, Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CategoryForm, ProductForm

class categoryView(View):
    def get(self, request):
        c=categories.objects.all()
        context={'categories':c}
        return render(request, template_name='category.html',context=context)

class productView(View):
    def get(self, request,i):
        c=categories.objects.get(id=i)
        context={'category':c}
        return render(request, template_name='product.html', context=context)

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('shop:categories')
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('shop:categories')
        return render(request, 'login.html', {'form': form})


# About page view
class AboutView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        context = {'product': product}
        return render(request, 'about.html', context=context)

    def post(self, request, id):
        product = Product.objects.get(id=id)
        if request.user.is_superuser:
            try:
                new_stock = int(request.POST.get('stock', 0))
                if new_stock > 0:
                    product.stock += new_stock
                    product.save()
                    messages.success(request, f"Stock updated. New stock: {product.stock}")
            except (ValueError, TypeError):
                messages.error(request, "Invalid stock value.")
        context = {'product': product}
        return render(request, 'about.html', context=context)

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:category')  # Update to your category list view name
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:add_product')  # Redirect to add_product page after submit
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})