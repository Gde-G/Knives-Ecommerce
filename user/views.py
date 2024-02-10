from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import Group

from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from cities_light.models import Country, Region, City

from django.db.utils import IntegrityError
from psycopg2.errors import UniqueViolation

from .models import MyUser
from .tokens import account_activation_token
from .decorators import user_not_authenticated
from .forms import *
from .utils import generate_random_password, generate_random_username
from payment.models import Address, CardUser, ProductBuyed, DiscountCode
from product.models import Product, Category, Handle, Message


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


def get_phone_prefix(request: HttpRequest):
    country_id = request.GET.get('country_id')
    country = get_object_or_404(Country, id=country_id)

    return JsonResponse({"code_phone": '+' + str(country.phone)})


@login_required(login_url='account_login')
def profile(request: HttpRequest):
    addresses = Address.objects.filter(owner=request.user)
    products_buyed = ProductBuyed.objects.filter(owner=request.user)
    cards_debit = CardUser.objects.filter(
        Q(user=request.user) & Q(card__type_card__iexact='debit'))
    cards_credit = CardUser.objects.filter(
        Q(user=request.user) & Q(card__type_card__iexact='credit'))

    context = {
        'addresses': addresses,
        'products': products_buyed,
        'cards_debit': cards_debit,
        'cards_credit': cards_credit
    }
    return render(request, 'account/profile.html', context=context)


def activate_with_email(request, user, to_email):
    try:
        mail_subject = "Bienvenido/a a Knife ecommerce simulation - Confirmación de Registro"

        context = {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }

        temp = get_template(
            'account/email/email_confirmation_message_our.html')

        content = temp.render(context)

        corr = EmailMultiAlternatives(
            subject=mail_subject,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )

        corr.attach_alternative(content, 'text/html')
        corr.send(fail_silently=False)

        messages.success(
            request, f'Hola {user}, ve a tu bandeja de entrada de correo electrónico {to_email} y haz clic en el enlace de activación recibido para confirmar y completar el registro. Nota: Verifica tu carpeta de correo no deseado (spam).')
    except:
        messages.error(
            request, f'Problema al enviar el correo electrónico de confirmación a {to_email}, verifica si lo has escrito correctamente.')


@user_not_authenticated
def sign_up(request: HttpRequest):
    form = MyUserCreationForm()
    countries = Country.objects.all()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()

            EmailAddress.objects.create(
                email=user.email, primary=True, user_id=user.pk)
            activate_with_email(request, user, form.cleaned_data.get('email'))

            return redirect('home')

        else:
            for field, error in form.errors.as_data().items():
                messages.error(request, f"ERROR: {field}, {error[0]}")

    context = {
        'page': 'sign-in',
        'form_sign': form,
        'countries': countries,
    }

    return render(request, 'account/signup.html', context=context)


def set_client_role(request: HttpRequest):
    if 'role' in request.session.keys():
        messages.info(
            request, f'Ya tiene el rol como {request.session["role"].capitalize()}. Si desea cambiarlo debera cerrar sesion.')
    else:
        request.session['role'] = 'client'

    return redirect(request.META['HTTP_REFERER'])


def create_staff_user(request: HttpRequest):
    if 'role' in request.session.keys():
        if request.session['role'] == 'staff':
            messages.info(
                request, 'Ya hemos mando al email ingresado las credenciales para que pueda iniciar sesion como staff! Recuerde revisar la casilla de "SPAM"')
            return redirect('account_login')
        else:
            return HttpResponseForbidden()
    else:
        request.session['role'] = 'staff'
        return redirect('sign-up-staff')


@user_not_authenticated
def sign_up_staff(request: HttpRequest):
    context = {'page': 'sign-in'}
    if 'role' not in request.session.keys():
        return redirect('create-staff-user')
    elif request.session['role'] != 'staff':
        return redirect('create-staff-user')
    else:
        username = 'staff_' + generate_random_username(5)
        password = generate_random_password()

        context['username'] = username
        context['password'] = password

    return render(request, 'user/sign-up-staff.html', context=context)


def setup_staff(request: HttpRequest):

    try:
        group, create = Group.objects.get_or_create(name='Staff')
        if EmailAddress.objects.filter(
            email=request.POST.get('email')).exists():
            return JsonResponse({
                'status': 'error',
                'text': 'Este correo ya esta vinculado a un usuario, pruebe con otro!'
            })
        user: MyUser = MyUser.objects.create_staff(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )

        user.groups.add(group)
        user.save()

    except (UniqueViolation, IntegrityError) as e:
        return JsonResponse({
            'status': 'error',
            'text': 'Este correo ya esta vinculado a un usuario, pruebe con otro!'})
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': f'{e}',
            'text': 'Estamos experimentando problemas. Intente mas tarde!'})
    try:
        mail_subject = "Bienvenido/a como Staff a Knife ecommerce simulation - Confirmación de Registro"

        context = {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }

        temp = get_template(
            'account/email/email_staff_confirmation.html')

        content = temp.render(context)

        corr = EmailMultiAlternatives(
            subject=mail_subject,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )

        corr.attach_alternative(content, 'text/html')
        corr.send(fail_silently=False)

        return JsonResponse({'status': 'success', 'email': user.email})
    except:
        return JsonResponse({'status': 'error', 'text': 'No hemos podido enviarle el correo a este email, intente con otro!'})


def activate_staff(request: HttpRequest, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
        email_address: EmailAddress = EmailAddress.objects.get(
            email=user.email)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        email_address.verified = True
        email_address.save()
        user.save()
        login(request, user, backend='user.authbackends.MyUserBackend')
        return redirect('staff-success')
    else:
        messages.error(request, 'Activation link is invalid!')
        request.session.delete()
        return redirect('home')


def staff_success(request: HttpRequest):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    return render(request, 'user/staff-success.html')


def staff_logout(request: HttpRequest):
    if request.user.is_authenticated and request.user.is_superuser != True:
        try:
            user = MyUser.objects.get(id=request.user.id)
            prod = Product.objects.filter(add_by=user)
            hand = Handle.objects.filter(add_by=user)
            cate = Category.objects.filter(add_by=user)
            dis_code = DiscountCode.objects.filter(add_by=user)
            reply_msg = Message.objects.filter(staff_user=user)
            email = EmailAddress.objects.filter(user=user)

            prod.delete()
            hand.delete()
            cate.delete()
            dis_code.delete()
            email.delete()
            
            for rep in reply_msg:
                rep.have_answered = False
                rep.staff_user = None
                rep.answer = None
                rep.save()

            user.is_active = False
            user.save()
            request.session.clear()

            logout(request)

        except (KeyError, Exception) as e:
            messages.error(
                request, "An error occurred during logout. Please try again.")

    else:
        logout(request)
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
        email_address: EmailAddress = EmailAddress.objects.get(
            email=user.email)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        email_address.verified = True
        email_address.save()
        user.save()

        messages.success(
            request, 'Gracias por comfirmar tu registro. Inicie sesion para empezar a interactuar!')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')


@user_not_authenticated
def fast_login(request: HttpRequest):
    form = MyUserLoginForm()
    if request.method == 'POST':
        form = MyUserLoginForm(request=request, data=request.POST)

        if form.is_valid():
            remember = form.cleaned_data['remember']

            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                if user.is_active:
                    login(request, user)

                    if not remember:
                        request.session.set_expiry(0)

                    messages.success(
                        request, f'Hi {user.username}, login success')
                else:
                    activate_with_email(request, user, user.email)
                    messages.error(
                        request, f"Su cuenta esta inactiva, para activarla ingrese al email con el cual se creo la cuenta y activela con el email que le mandamos al momento de crearse la cuenta!")
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, f"Ingrese bien los datos!")
        else:

            for field, error in form.errors.as_data().items():
                if field == "captcha" and error[0] == 'This field is required.':
                    messages.error(
                        request, "ERROR, you must pass the reCAPTCHA test.")
                    continue
                elif error[0] == 'This account is inactive.':
                    messages.error(
                        request, "This account is not active, check your email inbox to active.")
                elif field == '__all__':
                    messages.error(
                        request, "Error, introduzca un username y clave validos.")
                else:
                    messages.error(request, f"Error in: {field}. {error[0]}")

    context = {'formLogin': form}
    return render(request, 'core/index.html', context=context)


def inactive_account(request: HttpRequest):

    messages.info(request,
                  "This account in inactive, you have to check your email to activate it!")

    if 'HTTP_REFERER' in request.META.keys():
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('home')


def account_email_verification_sent(request: HttpRequest):
    messages.info(request, 'We have sent an e-mail to you for verification. Follow the link provided to finalize the signup process. If you do not see the verification e-mail in your main inbox, check your spam folder. Please contact us if you do not receive the verification e-mail within a few minutes.')
    return redirect('home')


@login_required(login_url='account_login')
def password_setup(request):

    user = MyUser.objects.get(pk=request.user.pk)
    print(user)
    form = MyUserSocialAccountSetForm(user)

    if user is not None:
        if SocialAccount.objects.filter(user=user).exists():
            if request.method == 'POST':
                form = MyUserSocialAccountSetForm(user, request.POST)
                if form.is_valid():
                    new_username = request.POST.get('username')
                    if MyUser.objects.filter(username=new_username).exists() and user.username != new_username:
                        messages.error(
                            request, f'That username ({new_username}) is already take, choose other!')
                        return redirect(request.META['HTTP_REFERER'])
                    else:
                        user.username = new_username
                    form.save()
                    user.save()

                    messages.success(
                        request, f"Congrats {user.username}, your account have been created succesfully! Login to access.")
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)

                return redirect('home')

        else:
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'user': user,
        'form': form
    }

    return render(request, 'user/password-setup-social.html', context=context)


def account_reset_password_done(request: HttpRequest):
    messages.info(request, 'We have sent you an e-mail. If you have not received it please check your spam folder. Otherwise contact us if you do not receive it in a few minutes.')
    return redirect('home')


def account_reset_password_from_key_done(request: HttpRequest):
    messages.success(request, 'Your password is now changed.')
    return redirect('home')


@login_required(login_url='account_login')
def update_profile(request: HttpRequest):
    user = MyUser.objects.get(id=request.user.id)
    countries = Country.objects.all()
    form = MyUserUpdateForm(instance=user)

    if user.profile_img:
        img_have = 'True'

    else:
        img_have = 'False'

    if request.method == 'POST':
        form = MyUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            messages.success(
                request, f'{user.username.capitalize()} your profile has been updated')

            return redirect('account_profile')
        else:
            for field, error in form.errors.as_data().items():
                if error[0] == 'Custom user with this Email already exists.':
                    messages.error(
                        request, f'Error in: {field.capitalize()}, that email is already used in other account. Try again!')
                else:
                    messages.error(
                        request, f'Error in: {field.capitalize()}, {error[0]} ')

    context = {
        'form': form,
        'user': user,
        'img_have': img_have,
        'countries': countries,
    }

    return render(request, 'user/update-profile.html', context=context)
