from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('privacy/', views.private_policy, name='privacy'),
    path('terms/', views.term_use, name='terms')
]
