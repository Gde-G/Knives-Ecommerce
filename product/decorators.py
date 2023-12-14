from django.core.exceptions import PermissionDenied
from .models import Product


def user_added_product_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        product_id = kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise PermissionDenied("Product not found")
        print(request.user.is_superuser)
        if product.add_by != request.user:
            if request.user.is_superuser == False:
                raise PermissionDenied(
                    "You are not allowed to access this product.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
