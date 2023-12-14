from django.http import HttpRequest

from .models import Cart, Category


def categories_list(request: HttpRequest):
    cates = Category.objects.all()
    
    return {'categories_cp': [x.name for x in cates]}


def amount_items_cart(request: HttpRequest):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(owner=request.user)
        amount = cart.items.all().count()

        return {'amount_prod_cart': amount}
    else:
        return {'amount_prod_cart': 0}
