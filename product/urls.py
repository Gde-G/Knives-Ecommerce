from django.urls import path
from . import views


urlpatterns = [
    path('prod/<str:prod>', views.get_product, name='prod'),
    path('products', views.get_products, name='products'),
    path('products/s/', views.search_prods, name='search-prods'),
    path('products/<str:category>', views.get_products_by_category,
         name='products_by_category'),


    path('cart/', views.get_cart, name='cart'),
    path('add-to-cart/<int:prod_id>', views.add_to_cart, name='add-to-cart'),
    path('del-from-cart/<int:prod_id>',
         views.delete_from_cart, name='delete-from-cart'),

    path('add-product/', views.create_product, name='add-product'),
    path('edit-product/<str:pk>', views.update_product, name='edit-product'),

    path('add-category/', views.create_cetegory, name='add-category'),

    path('add-handle/', views.create_handle, name='add-handle'),

    path('msg-info/<int:pk>', views.message_info, name='msg-info'),
    path('del-msg/<int:pk>', views.del_message, name='del-msg'),

    path('reply-msg/<int:pk>', views.reply_msg, name='add-reply'),
    path('edit-reply/<int:pk>', views.update_reply, name='edit-reply-msg'),
]
