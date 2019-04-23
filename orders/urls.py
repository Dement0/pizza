from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomLoginForm

# Add namespace to URLconf
app_name = 'orders'

urlpatterns = [

    # ex: /
    path('', views.IndexView.as_view(), name='index'),

    # ex: /1
    path('<int:pk>/', views.DetailView.as_view(), name='details'),

    path('cart/', views.view_cart, name='cart'),

    # ex: /login
    path('login/', views.login_view, name='login'),

    # ex: /logout
    path('logout/', views.logout_view, name='logout'),

    # ex: /signup
    path('signup/', views.signup_view, name='signup'),
]
