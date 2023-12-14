from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.template.loader import get_template
from django.contrib.admin.views.decorators import staff_member_required
from django.db.utils import IntegrityError

from urllib.parse import urlencode
from xhtml2pdf import pisa
from decimal import Decimal

from cities_light.models import Country, City, Region
from user.models import MyUser
from product.models import Cart, CartItems
from .models import Address, Order, OrderItem, Card, CardUser, ProductBuyed, DiscountCode
from .forms import AddressForm, CardForm, CreateDisCode
from .utils import *

import datetime
import holidays


def setting_checkout(request: HttpRequest):
    total = 0

    cart = Cart.objects.get(owner=request.user)
    cart_items = CartItems.objects.filter(cart=cart)
    order = Order.objects.create(
        owner=request.user,
        products_price=0,
        expiration_date=datetime.datetime.now() + datetime.timedelta(minutes=30)
    )

    for prod in cart_items:
        OrderItem.objects.create(
            order=order,
            product=prod.product,
        )
        total += float(prod.product.price)

    order.products_price = total
    order.total_to_pay = total
    order.save()

    return redirect('shipping', token=order.token)


def checkout_shipping(request: HttpRequest, token):
    order = get_object_or_404(Order, token=token)
    if order.status != 'incomplete':
        return redirect('finished-payment', token)
    address = Address.objects.filter(owner=order.owner).first()

    if address != None:
        if address.country.name == 'Argentina':
            shipping_to = 'national'
            days_to_add = 6
            shipping_price = 1000
        else:
            shipping_to = 'international'
            days_to_add = 15
            shipping_price = 5000

        holiday_days = holidays.country_holidays(address.country.code2)
        now_date = datetime.datetime.now()
        business_day = datetime.timedelta(days=1)

        while days_to_add > 0:
            now_date += business_day
            if now_date.weekday() >= 5 or now_date in holiday_days:
                continue
            days_to_add -= 1

        date_arrives = str(get_day_name(now_date) + " " +
                           str(now_date.day) + ' de ' + get_month_name(now_date))

    else:
        date_arrives = datetime.datetime.now() + datetime.timedelta(days=5)
        shipping_to = ''
        shipping_price = ''
    if request.method == 'POST':
        shipping_method = request.POST.get('shipping_kind')
        order.shipping_method = shipping_method

        if shipping_method == 'delivery':
            if address == None:
                messages.error(
                    request, 'Dirección para el envio no ingresada!')
                return redirect('shipping', token)
            order.address = address
            order.shipping_price = shipping_price
            order.total_to_pay += shipping_price
            order.shipping_arrives = now_date
        else:
            order.shipping_price = 0
        order.save()
        return redirect('payment', token)

    context = {
        'token': token,
        'address': address,
        'order': order,
        'date_arrives': date_arrives,
        'shipping_to': shipping_to,
        'shipping_price': shipping_price
    }
    return render(request, 'payment/buy-shipping.html', context=context)


def shipping_addresses(request: HttpRequest, token):
    addresses = Address.objects.filter(owner=request.user)

    if request.method == 'POST':

        choseen_address = Address.objects.get(
            id=request.POST.get("choosen_address"))

        choseen_address.choosen_at = datetime.datetime.now()
        choseen_address.save()

        return redirect('shipping', token)
    context = {
        'addresses': addresses,
        'token': token
    }
    return render(request, 'payment/shipping-addresses.html', context=context)


def get_regions(request: HttpRequest):
    country_id = request.GET.get('country_id')
    country = get_object_or_404(Country, id=country_id)

    regions_of_country = Region.objects.filter(country=country)

    regions_data = {region.pk: region.name for region in regions_of_country}

    return JsonResponse(regions_data, safe=False)


def get_cities(request: HttpRequest):
    region_id = request.GET.get('region_id')

    region = get_object_or_404(Region, id=region_id)
    cities_of_region = City.objects.filter(region=region)

    cities_data = {
        city.pk: city.name for city in cities_of_region}

    return JsonResponse(cities_data)


def add_address(request, token):
    countries = Country.objects.all()
    address_type = Address.address_type_choices

    form = AddressForm()

    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)
            address.owner = request.user
            address.save()

            messages.success(request, 'Address been created successfully!')
            return redirect('shipping', token)
        else:
            for field, error in form.errors.as_data().items():
                messages.error(request, f'ERROR. {field}, {error[0]}')

    context = {
        'countries': countries,
        'address_type_choices': address_type,
        'token': token
    }
    return render(request, 'payment/add-address.html', context=context)


def edit_address(request, token, id):
    address = Address.objects.get(id=id)

    address_type = Address.address_type_choices

    form = AddressForm(instance=address)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.choosen_at = datetime.datetime.now()
            address.save()

            return redirect('shipping', token)

        else:
            for field, error in form.errors.as_data().items():
                messages.error(request, f'ERROR. {field}, {error[0]}')

    context = {
        'token': token,
        'address_type': address_type,
        'address': address
    }

    return render(request, 'payment/edit-address.html', context=context)


def del_address(request, token, id):
    try:
        address = Address.objects.get(id=id)
        address.delete()
        return JsonResponse({'result': 'success'})
    except:
        return JsonResponse({'result': 'error'})


def checkout_payment(request: HttpRequest, token):
    order = get_object_or_404(Order, token=token)

    if order.status != 'incomplete':
        return redirect('finished-payment', token)

    card = CardUser.objects.filter(user=request.user).first()

    if card == None:
        card = ''

    discount_shipping = DiscountCode.objects.filter(
        discount_kind='Shipping', enabled_from__lte=datetime.date.today(), enabled_to__gte=datetime.date.today())
    discount_percentage = DiscountCode.objects.filter(
        discount_kind='Total',  enabled_from__lte=datetime.date.today(), enabled_to__gte=datetime.date.today())

    if request.method == 'POST':
        discount_code = request.POST.get("discount_code")
        kind = request.POST.get("payment_kind")

        if discount_code != '' and order.discount_code == None:
            discount = DiscountCode.objects.get(code=discount_code)
            order.discount_code = discount
            if discount.discount_kind == 'Total':
                order.discount_amount = calc_discount(
                    discount.discount, order.total_to_pay)

            elif order.shipping_method != 'local':
                order.discount_amount = calc_discount(
                    discount.discount, order.shipping_price)

            order.total_to_pay -= Decimal(order.discount_amount)

        order.pay_method = kind
        order.save()
        if kind == "registered":
            order.pay_method_card = card
            order.save()

            return redirect('confirm-payment', token)
        elif kind == 'credit' or kind == 'debit':
            return redirect('add-card', token, kind)
        elif kind == 'cash':
            return redirect('cash-payment', token)
        elif kind == 'wallet':
            return redirect('wallet-payment', token)
        else:
            messages.error(
                request, 'Plis select one of the options.')

    context = {
        'token': token,
        'order': order,
        'card': card,
        'discount_shipping': discount_shipping,
        'discount_percentage': discount_percentage
    }
    return render(request, 'payment/buy-payment.html', context=context)


@staff_member_required
def create_dis_code(request: HttpRequest):
    if request.method == 'POST':
        form = CreateDisCode(request.POST)
        if form.is_valid():
            try:
                dis_code = form.save(commit=False)
                dis_code.add_by = request.user
                dis_code.save()

                return JsonResponse({'status': 'success', 'message': f'Codigo de Descuento: {dis_code.code}, Creado exitosamente!'})
            except IntegrityError:
                return JsonResponse({'status': 'error', 'message': 'Ya existe una descuento con ese codigo.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Alguna de las entradas tiene datos invalidos, intente nuevamente!'})

    else:
        return HttpResponseBadRequest()


def discount_codes(request: HttpRequest):
    code_name = request.GET.get('code_name')
    discount_code = DiscountCode.objects.filter(code=code_name).first()

    if discount_code == None:
        return JsonResponse({'result': 'error'})
    else:
        return JsonResponse({'result': 'success'})


def add_card_payment(request: HttpRequest, token, kind):
    order = Order.objects.get(token=token)
    types_id = Card.id_type_choices
    form = CardForm()
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = Card.objects.filter(
                Q(number__iexact=request.POST.get('number')) & Q(
                    expirate_date__iexact=request.POST.get('expirate_date')) & Q(
                    cvv__iexact=request.POST.get('cvv')) & Q(
                    name__iexact=request.POST.get('name')) & Q(
                    type_id__iexact=request.POST.get('type_id')) & Q(
                    number_id__iexact=request.POST.get('number_id')) & Q(
                    type_card__iexact=kind)
            ).first()
            if card != None:
                CardUser.objects.create(card=card, user=request.user)
                return redirect('payment', token)
            else:
                messages.error(
                    request, 'Datos incorrectos! Recuerde usar los datos de las tarjetas de prueba.')
        else:
            for field, error in form.errors.as_data().items():
                messages.error(request, f'{field}, {error}')
    context = {
        'token': token,
        'order': order,
        'kind': kind,
        'types_id': types_id,
        'form': form
    }
    return render(request, 'payment/add-card.html', context=context)


def get_cards(request: HttpRequest, token):
    order = get_object_or_404(Order, token=token)
    if order.status != 'incomplete':
        return redirect('finished-payment', token)
    cards = CardUser.objects.filter(user=request.user)

    if request.method == 'POST':

        card = CardUser.objects.get(id=request.POST.get('choosen_card'))
        card.save()
        return redirect('payment', token)
    context = {
        'token': token,
        'order': order,
        'cards': cards
    }
    return render(request, 'payment/payment-cards.html', context=context)


def delete_card(request: HttpRequest, token, id):
    pass


def cash_payment(request: HttpRequest, token):
    order = get_object_or_404(Order, token=token)
    if order.status != 'incomplete':
        return redirect('finished-payment', token)

    if request.method == 'POST':

        order.paymethod_cash_type = request.POST.get('cash_kind')
        order.save()
        return redirect('confirm-payment', token)
    context = {
        'order': order
    }
    return render(request, 'payment/cash-payment.html', context=context)


def wallet_payment(request: HttpRequest, token):
    order = get_object_or_404(Order, token=token)
    if order.status != 'incomplete':
        return redirect('finished-payment', token)
    if request.method == 'POST':

        order.paymethod_wallet_type = request.POST.get('wallet_kind')
        order.save()
        return redirect('confirm-payment', token)
    context = {
        'order': order
    }
    return render(request, 'payment/wallet-payment.html', context=context)


def confirm_payment(request: HttpRequest, token):
    order = get_object_or_404(Order, token=token)
    if order.status != 'incomplete':
        return redirect('finished-payment', token)
    orders_items = OrderItem.objects.filter(order=order)

    if order.paymethod_cash_type != None and order.emition_cash_date == None:
        order.emition_cash_date = timezone.now()
        order.expiration_cash_date = timezone.make_aware(
            datetime.datetime.now() + datetime.timedelta(days=7))
        order.save()

    context = {
        'token': token,
        'order': order,
        'products': orders_items,
    }
    return render(request, 'payment/confirm-payment.html', context=context)


def render_pdf_view(request: HttpRequest, token):
    order = Order.objects.get(token=token)
    order_items = OrderItem.objects.filter(order=order)
    template_path = 'payment/simulation-cash-payment.html'
    context = {
        'order': order,
        'order_items': order_items,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="knife-ecommerce-buy-order-{timezone.now()}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def process_payment(request: HttpRequest, token):
    status = request.GET.get('status')
    order = Order.objects.get(token=token)

    if order.owner != request.user:
        return JsonResponse({'retrun': 'error'})
    if order.status == 'approved' or order.status == 'denied':
        return JsonResponse({'retrun': 'error'})

    order_items = OrderItem.objects.filter(order=order)
    cart = Cart.objects.get(owner=request.user)

    if status == 'approved':
        order.status = status
        order.billing_status = True
        order.pay_received_date = timezone.now()
        order.save()
        for item in order_items:
            ProductBuyed.objects.create(
                owner=request.user, product=item.product,
                order=order)
            item.product.quantity -= 1
            if item.product.quantity < 1:
                item.product.stock = False
            item.product.save()

        cart.clear_cart()

        cart.save()
    elif status == 'pending':
        order.status = status
        order.save()

        cart.clear_cart()
        order.save()
    elif status == 'denied':
        order.status = status
        order.save()
    else:
        return JsonResponse({'retrun': 'error'})

    return JsonResponse({'return': 'success'})


def finished_payment(request: HttpRequest, token):

    order = Order.objects.get(token=token)
    if order.owner == request.user:
        order_items = OrderItem.objects.filter(order=order)

        if order.status == 'approved':
            try:
                if order.shipping_method == 'local':

                    opt2 = timezone.now() > order.pay_received_date + \
                        datetime.timedelta(minutes=10)
                    opt3 = timezone.now() > order.pay_received_date + \
                        datetime.timedelta(hours=1, minutes=18)
                    opt4 = False
                    opt4_date = ''
                    if opt2:
                        opt2_date = order.pay_received_date + \
                            datetime.timedelta(minutes=10)
                    else:
                        opt2_date = ''

                    if opt3:
                        opt3_date = order.pay_received_date + \
                            datetime.timedelta(hours=1, minutes=18)
                    else:
                        opt3_date = ''

                elif order.shipping_method == 'delivery':
                    opt2 = timezone.now() > order.pay_received_date + datetime.timedelta(days=1)
                    opt3 = timezone.now() > order.pay_received_date + \
                        datetime.timedelta(days=1, minutes=7)
                    opt4 = datetime.date.today() > order.shipping_arrives

                    if opt2:
                        opt2_date = order.pay_received_date + \
                            datetime.timedelta(days=1, minutes=15)
                    else:
                        opt2_date = ''

                    if opt3:
                        opt3_date = order.pay_received_date + \
                            datetime.timedelta(days=1, minutes=7)
                    else:
                        opt3_date = ''

                    if opt4:
                        opt4_date = order.shipping_arrives
                    else:
                        opt4_date = ''
                else:
                    opt2 = False
                    opt2_date = ''
                    opt3 = False
                    opt3_date = ''
                    opt4 = False
                    opt4_date = ''
            except:
                opt2 = False
                opt2_date = ''
                opt3 = False
                opt3_date = ''
                opt4 = False
                opt4_date = ''
        else:
            opt2 = False
            opt2_date = ''
            opt3 = False
            opt3_date = ''
            opt4 = False
            opt4_date = ''
    else:
        return HttpResponseForbidden()
    context = {
        'order': order,
        'order_items': order_items,
        'opt2': opt2,
        'opt2_date': opt2_date,
        'opt3': opt3,
        'opt3_date': opt3_date,
        'opt4': opt4,
        'opt4_date': opt4_date,
    }

    return render(request, 'payment/finished-payment.html', context=context)


def trans_pend_to_apro(request: HttpRequest, token):
    order = Order.objects.get(token=token)
    if order.status == 'pending' and request.user == order.owner:

        redirect_url = reverse(
            'process-payment', args=[token]) + f"?status=approved"
        return redirect(redirect_url)
    return HttpResponseBadRequest()


def trans_pend_to_deni(request: HttpRequest, token):
    order = Order.objects.get(token=token)
    if order.status == 'pending' and request.user == order.owner:
        redirect_url = reverse(
            'process-payment', args=[token]) + f"?status=denied"
        return redirect(redirect_url)
    return HttpResponseBadRequest()
