from typing import Any, Dict, Optional
from django.contrib import admin

from functools import update_wrapper
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponseRedirect, HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse

from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout

from user.models import MyUser
from product.models import Category, Handle, Product, Prod_SecImg, Message
from payment.models import DiscountCode


class MyAdminSite(admin.AdminSite):

    def admin_view(self, view, cacheable=False):
        def inner(request: HttpRequest, *args, **kwargs):

            if not self.has_permission(request) or not ('role' in request.session.keys() and request.session['role'] == 'staff'):
                if request.path == reverse('admin:logout', current_app=self.name):
                    index_path = reverse('admin:index', current_app=self.name)
                    return HttpResponseRedirect(index_path)
                raise Http404()
            return view(request, *args, **kwargs)
        if not cacheable:
            inner = never_cache(inner)

        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def logout(self, request: HttpRequest, extra_context: Dict[str, Any] | None = ...):
        if request.user.is_authenticated and request.user.is_superuser != True:
            try:
                user = MyUser.objects.get(id=request.user.id)
                prod = Product.objects.filter(add_by=user)
                hand = Handle.objects.filter(add_by=user)
                cate = Category.objects.filter(add_by=user)
                dis_code = DiscountCode.objects.filter(add_by=user)
                reply_msg = Message.objects.filter(staff_user=user)

                prod.delete()
                hand.delete()
                cate.delete()
                dis_code.delete()

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
