from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.urls import reverse_lazy
from .views import (index, api_get, api_put, login, register,
                    logout, add_quote, password_reset,
                    password_reset_confirm, my_quotes)
from django.contrib.auth.views import (LogoutView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView
                                       )


urlpatterns = [
    path('', index, name='index'),
    path('api/get/<str:table>/<str:quote_type>/', api_get, name='api_get'),
    path('api/put/<str:table>/', api_put, name='api_put'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('add_quote/', add_quote, name='add_quote'),
    path('my_quotes/', my_quotes, name='my_quotes'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete')
]