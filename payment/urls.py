from django.urls import path
from . import views

urlpatterns = [
    path('get-regions', views.get_regions, name='get-regions'),
    path('get-cities', views.get_cities, name='get-cities'),
    path('discount-codes', views.discount_codes, name='get-discount-codes'),
    path('add-dis-code/', views.create_dis_code, name='add-discode'),
    path('checkout/', views.setting_checkout, name='checkout'),

    path('checkout/<str:token>/shipping',
         views.checkout_shipping, name='shipping'),
    path('checkout/<str:token>/shipping/addresses',
         views.shipping_addresses, name="addresses"),
    path('checkout/<str:token>/shipping/add-new/',
         views.add_address, name='add-address'),
    path('checkout/<str:token>/shipping/edit-address/<str:id>',
         views.edit_address, name='edit-address'),
    path('checkout/<str:token>/shipping/del-address/<str:id>',
         views.del_address, name='del-address'),

    path('checkout/<str:token>/payment',
         views.checkout_payment, name='payment'),
    path('checkout/<str:token>/payment/add-card/<str:kind>',
         views.add_card_payment, name="add-card"),
    path('checkout/<str:token>/payment/cards',
         views.get_cards, name='get-cards'),
    path('checkout/<str:token>/payment/cash',
         views.cash_payment, name='cash-payment'),
    path('checkout/<str:token>/payment/wallet',
         views.wallet_payment, name='wallet-payment'),

    path('checkout/<str:token>/payment/confirm/',
         views.confirm_payment, name='confirm-payment'),
    path('checkout/<str:token>/payment/confirm/pdf',
         views.render_pdf_view, name='order-pay-pdf'),

    path('checkout/<str:token>/process-payment',
         views.process_payment, name='process-payment'),
    path('checkout/<str:token>/finished-payment',
         views.finished_payment, name="finished-payment"),
    path('checkout/<str:token>/trans-apro',
         views.trans_pend_to_apro, name="trans-apro"),
    path('checkout/<str:token>/trans-deni',
         views.trans_pend_to_deni, name="trans-deni"),

]
