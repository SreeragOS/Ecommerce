from django.shortcuts import render
from django.views import View
from shop.models import Product
from cart.models import Cart
from django.shortcuts import redirect
from .forms import OrderForm
import razorpay
import uuid
from cart.models import Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import login
class AddToCart(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)
        return redirect('cart:cartdetail')
class CartDetail(View):
    def get(self, request):
        user = request.user
        cart_items = []
        if user.is_authenticated:
            cart_items = Cart.objects.filter(user=user)
        # Calculate subtotal
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'subtotal': subtotal})
class Cartdecrement(View):
    def get(self, request, id):
        cart_item = Cart.objects.get(id=id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart:cartdetail')
class Cartdelete(View):
    def get(self, request, id):
        cart_item = Cart.objects.get(id=id)
        cart_item.delete()
        return redirect('cart:cartdetail')
class CheckoutView(View):
    def post(self, request):
        print(request.POST)
        form_instance=OrderForm(request.POST)   
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u= request.user
            o.user=u
            cart_items=Cart.objects.filter(user=u)
            total=0
            for item in cart_items:
                total+=item.subtotal()
            print(total)
            o.total_amount=total
            o.save()
            if o.payment_method=="Online":
                client=razorpay.Client(auth=("rzp_test_S6TDJZMf8LYQCX","wdoMCcaaOqWgiakigm3HkGWT"))
                print(client)
                payment_response=client.order.create(dict(amount=int(total)*100, currency="INR"))
                print(payment_response)
                id=payment_response['id']
                o.order_id=id
                o.save()
                context={'payment':payment_response}
                return render(request, 'payment.html',context)
            else:
                id=uuid.uuid4().hex[:14]
                o.order_id='order_COD'+id
                o.is_ordered=True
                o.save()
                for i in cart_items:
                    items=OrderItem.objects.create(order=o,product=i.product,quantity=i.quantity) 
                    items.save()
                    items.product.stock-=items.quantity
                    items.product.save()
                cart_items.delete()
                return render(request, 'payment.html')

    def get(self, request):
        form_instance=OrderForm()
        context={'form':form_instance}
        return render(request, 'checkout.html',context)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class paymentsuccess(View):
    def post(self, request,i):
        u=User.objects.get(username=i)
        login(request,u)
        id=request.POST['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        o.is_ordered=True
        o.save()
        cart_items=Cart.objects.filter(user=request.user)
        for i in cart_items:
            items=OrderItem.objects.create(order=o,product=i.product,quantity=i.quantity) 
            items.save()    
            items.product.stock-=items.quantity
            items.product.save()
        cart_items.delete()    
        return render(request, 'paymentsuccess.html')
class Ordersummary(View):
    def get(self, request):
        u=request.user
        orders=Order.objects.filter(user=u,is_ordered=True).order_by('-order_date')
        context={'orders':orders}
        return render(request, 'orders.html',context)