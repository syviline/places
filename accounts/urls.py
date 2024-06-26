from .views import register_request, VerificationView, mail_confirm

from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    path('signup/', register_request, name='signup'),

    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # мы отправляем письмо  с потвердением
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # после формы
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # мы получаем код  с потвердением
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # после этого
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
    path('mail-confirm', mail_confirm, name='mail_confirm')
]