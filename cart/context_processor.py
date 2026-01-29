from .models import Cart
def count(request):
    count = 0
    if request.user.is_authenticated:
        u = request.user
        c = Cart.objects.filter(user=u)
        try:
            for i in c:
                count += i.quantity
            return {'cart_count': count}
        except:
            return {'cart_count': 0}
    return {'cart_count': 0}