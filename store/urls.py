# /home/siisi/e-commerce/store/urls.py

from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('create_product/', views.create_product, name='create_product'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('categories/', views.category_list, name='category_list'),
    path('search/', views.search, name='search'),

]
