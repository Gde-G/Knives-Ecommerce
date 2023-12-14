from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Max, Q
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from user.models import MyUser

from .forms import *
from .models import Category, Handle, Product, Prod_SecImg, Cart, CartItems
from .filters import ProductFilter
from .decorators import user_added_product_required

import datetime


def prod_paginator(obj_list, pages):
    paginator = Paginator(object_list=obj_list, per_page=9)

    try:
        products = paginator.get_page(pages)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return products


def get_product(request: HttpRequest, prod):
    product = Product.objects.get(name=prod)
    prod_sec_img = Prod_SecImg.objects.get(prod=product.id)

    similar_prods = Product.objects.filter(
        Q(category=product.category) & ~Q(id=product.id))[:3]
    if len(similar_prods) < 3:
        similar_prods = Product.objects.all()[:3]

    show_ques = request.GET.get('show')

    if show_ques == 'all':
        msgs = product.comments.all()
    else:
        msgs = product.comments.all()[:3]

    formMsg = CreateMessage()

    if request.method == 'POST':
        formMsg = CreateMessage(request.POST)

        if formMsg.is_valid():

            msg = formMsg.save(commit=False)
            msg.user = request.user
            msg.product = product

            msg.save()
            messages.info(
                request, 'Question be maked, soon it will be answered!')

            return redirect(request.META['HTTP_REFERER'])

        else:
            for field, error in formMsg.errors.as_data().items():
                messages.error(request, f'ERROR. {field}, {error[0]}')

    context = {
        'prod': product,
        'similar_prods': similar_prods,
        'similar_prods_len': len(similar_prods),
        'sec_img': prod_sec_img,
        'questions': msgs,
        'amount_ques': product.comments.count(),
        'show_ques': show_ques,

    }

    return render(request, 'product/prod.html', context=context)


def get_products(request: HttpRequest):
    products = Product.objects.all()
    prod_more_expensive = Product.objects.aggregate(Max('price'))
    max_price = int(prod_more_expensive['price__max']
                    ) if prod_more_expensive['price__max'] != None else 0
    all_categories = Category.objects.all()

    date_today = datetime.date.today()

    sort_by = request.GET.get('sort')
    if sort_by == 'hp':
        products = Product.objects.order_by('-price')
    elif sort_by == 'lp':
        products = Product.objects.order_by('price')
    else:
        sort_by = ''

    products_filter = ProductFilter(request.GET, products)

    products = prod_paginator(
        obj_list=products_filter.qs, pages=request.GET.get('p'))

    if request.GET.get('price__lte'):
        price_fil = True
    else:
        price_fil = False

    context = {
        'products': products,
        'products_filter': products_filter,
        'categories': all_categories,
        'sort_by': sort_by,
        'max_price': max_price,
        'price_fil': price_fil,
        'price__lte': request.GET.get('price__lte'),
        'price__gte': request.GET.get('price__gte'),
        'date_today': date_today.strftime('%Y-%m-%d')
    }

    return render(request, 'product/products.html', context=context)


def search_prods(request: HttpRequest):
    query = request.GET.get('query') if request.GET.get(
        'query') != None else ''

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(blade_material__icontains=query) |
        Q(blade_size__icontains=query) |
        Q(handle__material__icontains=query) |
        Q(description__icontains=query)
    )

    prod_more_expensive = Product.objects.aggregate(Max('price'))
    max_price = int(prod_more_expensive['price__max'])
    all_categories = Category.objects.all()

    sort_by = request.GET.get('sort')
    if sort_by == 'hp':
        products = Product.objects.order_by('-price')
    elif sort_by == 'lp':
        products = Product.objects.order_by('price')
    else:
        sort_by = ''

    products_filter = ProductFilter(request.GET, products)

    products = prod_paginator(
        obj_list=products_filter.qs, pages=request.GET.get('p'))

    if request.GET.get('price__lte'):
        price_fil = True
    else:
        price_fil = False

    context = {
        'query': query,
        'products': products,
        'products_filter': products_filter,
        'categories': all_categories,
        'sort_by': sort_by,
        'max_price': max_price,
        'price_fil': price_fil,
        'price__lte': request.GET.get('price__lte'),
        'price__gte': request.GET.get('price__gte')
    }

    return render(request, 'product/products.html', context=context)


def get_products_by_category(request: HttpRequest, category: str):
    all_categories = Category.objects.all()
    prod_more_expensive = Product.objects.aggregate(Max('price'))
    max_price = int(prod_more_expensive['price__max'])

    products_filter = ProductFilter(request.GET, Product.objects.filter(
        category__name__iexact=category))

    sort_by = request.GET.get('sort')
    if sort_by == 'hp':
        products = prod_paginator(
            obj_list=products_filter.qs.order_by('-price'),
            pages=request.GET.get('p')
        )
    elif sort_by == 'lp':
        products = prod_paginator(
            obj_list=products_filter.qs.order_by('price'),
            pages=request.GET.get('p')
        )
    else:
        products = prod_paginator(
            obj_list=products_filter.qs,
            pages=request.GET.get('p')
        )

    if request.GET.get('price__lte'):
        price_fil = True
    else:
        price_fil = False

    context = {
        'products': products,
        'products_filters': products_filter,
        'categories': all_categories,
        'sort_by': request.GET.get('sort'),
        'max_price': max_price,
        'price_fil': price_fil,
        'price__lte': request.GET.get('price__lte'),
        'price__gte': request.GET.get('price__gte')
    }

    return render(request, 'product/products.html', context=context)


def get_cart(request: HttpRequest):
    owner = MyUser.objects.get(username=request.user)
    cart, created = Cart.objects.get_or_create(owner=owner)
    total = 0
    try:
        cartItems = CartItems.objects.filter(cart=cart)
        for item in cartItems:
            total += float(item.product.price)

    except CartItems.DoesNotExist:
        cartItems = False
        total = 0

    context = {
        'cart': cart,
        'prods': cartItems,
        'cartItems': cartItems,
        'total_to_pay': total
    }
    return render(request, 'product/cart.html', context=context)


def add_to_cart(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)
    cart, created = Cart.objects.get_or_create(owner=request.user)
    cart_item = CartItems.objects.filter(cart=cart, product=product).first()

    if request.method == 'POST':
        if cart_item:
            messages.info(request, 'This product is already in your cart')
        else:
            cart_item = CartItems.objects.create(cart=cart, product=product)

    return redirect('cart')


def delete_from_cart(request: HttpRequest, prod_id):

    cart_item = CartItems.objects.filter(
        cart=Cart.objects.get(owner=request.user),
        product=get_object_or_404(Product, pk=prod_id)).first()

    if request.method == 'POST':
        try:
            cart_item.delete()
        except:
            messages.error(
                request, 'Something wrong! Try delete the product of the cart again.')

    return redirect('cart')


@staff_member_required(login_url="account_login")
def create_product(request: HttpRequest):
    formProd = CreateProduct()
    formSecImg = CreateProd_SecImg()

    all_categories = Category.objects.all()
    all_handles = Handle.objects.all()

    if request.method == 'POST':
        formProd = CreateProduct(request.POST, request.FILES)
        formSecImg = CreateProd_SecImg(request.POST, request.FILES)

        if all([formProd.is_valid(), formSecImg.is_valid()]):
            prod = formProd.save(commit=False)
            prod.name = prod.name.lower()
            prod.add_by = request.user
            prod.save()
            sec_img = formSecImg.save(commit=False)
            sec_img.img_sec_1 = prod.img_primary
            sec_img.prod = prod
            sec_img.save()

            messages.success(
                request, f'{prod.name.capitalize()} has been created')
            return redirect('products')
        else:
            for field, error in formProd.errors.as_data().items():
                messages.error(request, f'ERROR: {field}, {error[0]}')

            for field, error in formSecImg.errors.as_data().items():
                messages.error(request, f'ERROR: {field}, {error[0]}')

    context = {
        'all_categories': all_categories,
        'all_handles': all_handles
    }
    return render(request, 'product/add-edit-product.html', context=context)


@user_added_product_required
@staff_member_required(login_url="account_login")
def update_product(request: HttpRequest, pk):
    all_categories = Category.objects.all()
    all_handles = Handle.objects.all()

    prod = Product.objects.get(id__exact=int(pk))
    sec_imgs = Prod_SecImg.objects.get(prod__exact=prod)
    formProd = CreateProduct(instance=prod)
    formSecImg = CreateProd_SecImg(instance=sec_imgs)

    if request.method == 'POST':
        formProd = CreateProduct(request.POST, request.FILES, instance=prod)
        formSecImg = CreateProd_SecImg(
            request.POST, request.FILES, instance=sec_imgs)

        if all([formProd.is_valid(), formSecImg.is_valid()]):
            prod = formProd.save(commit=False)
            prod.name = prod.name.lower()
            prod.save()

            sec_img = formSecImg.save(commit=False)
            sec_img.img_sec_1 = prod.img_primary
            sec_img.save()

            messages.success(
                request, f'{prod.name.capitalize()} has been updated!')
            return redirect('products')

        else:

            for field, error in formProd.errors.as_data().items():
                messages.error(request, f'ERROR: {field}, {error[0]}')

            for field, error in formSecImg.errors.as_data().items():
                messages.error(request, f'ERROR: {field}, {error[0]}')

    context = {
        'page': 'update',
        'all_categories': all_categories,
        'all_handles': all_handles,
        'prod': prod,
        'sec_imgs': sec_imgs,
    }

    return render(request, 'product/add-edit-product.html', context=context)


@staff_member_required(login_url="account_login")
def create_cetegory(request: HttpRequest):
    if request.method == 'POST':
        formCate = CreateCategory(request.POST)

        if formCate.is_valid():
            try:
                cate = formCate.save(commit=False)
                cate.name = cate.name.lower()
                cate.add_by = request.user
                cate.save()

                return JsonResponse({'status': 'success', 'message': f'{cate.name.capitalize()} se creo de manera exitosa!'})

            except IntegrityError:
                return JsonResponse({'status': 'error', 'message': 'Ya existe una categoria con ese nombre.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Alguno de los datos ingresados es invalido, intente nuevamente!'})

    else:
        return HttpResponseBadRequest()


@staff_member_required(login_url="account_login")
def create_handle(request: HttpRequest):
    if request.method == 'POST':
        formHandle = CreateHandle(request.POST)

        if formHandle.is_valid():
            try:
                hand = formHandle.save(commit=False)
                hand.material = hand.material.lower()
                hand.add_by = request.user
                hand.save()

                return JsonResponse({'status': 'success', 'material': hand.material.capitalize()})

            except IntegrityError:
                return JsonResponse({'status': 'error', 'message': 'Ya existe una empuñadura de ese material!'})

        else:
            result = {'status': 'error',
                      'message': 'Error en el material, pruebe nuevamente.'}

            return JsonResponse(result)
    else:
        return HttpResponseBadRequest()


@staff_member_required(login_url="account_login")
def message_info(request: HttpRequest, pk):
    msg = Message.objects.get(id=int(pk))

    show_ques = request.GET.get('show')

    context = {
        'msg': msg,
        'show_ques': show_ques
    }
    return render(request, 'product/msg-info.html', context=context)


@staff_member_required(login_url="account_login")
def del_message(request: HttpRequest, pk):
    msg = Message.objects.get(id=int(pk))

    if request.method == 'POST':
        msg.delete()
        messages.success(request, f'Message by {msg.user} be deleted!')

        return redirect(request.META['HTTP_REFERER'])

    context = {'msg': msg}

    return render(request, 'product/del-msg.html', context=context)


@staff_member_required(login_url="account_login")
def reply_msg(request: HttpRequest, pk):
    msg = Message.objects.get(id=int(pk))
    formReply = CreateMessageAwnser()

    if request.method == 'POST':
        formReply = CreateMessageAwnser(request.POST, instance=msg)
        if formReply.is_valid():

            ans = formReply.save(commit=False)
            ans.staff_user = request.user
            ans.have_answered = True
            ans.save()

            messages.info(
                request, 'Reply post succesfully')

            return redirect(request.META['HTTP_REFERER'])
        else:
            for field, error in formReply.errors.as_data().items():
                messages.error(request, f'ERROR. {field}, {error[0]}')

            return redirect(request.META['HTTP_REFERER'])

    context = {
        'msg': msg,
        'formReply': formReply
    }
    return render(request, 'product/reply-msg.html', context=context)


@staff_member_required(login_url="account_login")
def update_reply(request: HttpRequest, pk):
    msg = Message.objects.get(id=int(pk))
    formReply = CreateMessageAwnser(instance=msg)

    if request.method == 'POST':
        formReply = CreateMessageAwnser(request.POST, instance=msg)

        if formReply.is_valid():
            ans = formReply.save(commit=False)
            ans.save()

            messages.info(
                request, 'Reply edit succesfully')

            return redirect(request.META['HTTP_REFERER'])
        else:
            for field, error in formReply.errors.as_data().items():
                messages.error(request, f'ERROR. {field}, {error[0]}')

            return redirect(request.META['HTTP_REFERER'])

    context = {
        'msg': msg,
        'formReply': formReply,
        'page': 'update'
    }
    return render(request, 'product/reply-msg.html', context=context)
