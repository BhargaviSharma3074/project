from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('view-products/', views.view_products, name='view_products'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('verify-product/', views.verify_product, name='verify_product'),
]

