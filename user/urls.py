from django.urls import path
from .import views

urlpatterns = [

    path('get-regions', views.get_regions, name='get-regions'),
    path('get-cities', views.get_cities, name='get-cities'),
    path('get-phone-code', views.get_phone_prefix, name='get-phone-prefix'),

    path('profile/', views.profile, name='account_profile'),
    path('edit-profile/', views.update_profile, name='edit-profile'),
    path('password-set/',
         views.password_setup, name='password_set'),
    path('login/', views.fast_login, name='login-page'),
    path('set-client-role/', views.set_client_role, name="set-client-role"),

    path('create-staff-user/', views.create_staff_user, name="create-staff-user"),
    path('sign-up-staff', views.sign_up_staff, name="sign-up-staff"),
    path('setup-staff/', views.setup_staff, name="staff-setup"),
    path('staff-confirm-email/<uidb64>/<token> ',
         views.activate_staff, name='staff_confirm_email'),
    path('staff-success/', views.staff_success, name='staff-success'),
    path('staff-logout/', views.staff_logout, name='staff-logout'),

    path('accounts/password/reset/done/', views.account_reset_password_done,
         name='account_reset_password_done'),
    path('accounts/signup/', views.sign_up, name='account_signup'),
    path('accounts/inactive/', views.inactive_account, name='account_inactive'),
    path('accounts/confirm-email/', views.account_email_verification_sent,
         name='account_email_verification_sent'),
    path('accounts/confirm-email/<uidb64>/<token> ',
         views.activate, name='account_confirm_email'),
    path('accounts/password/reset/key/done/', views.account_reset_password_from_key_done,
         name='account_reset_password_from_key_done'),

]
