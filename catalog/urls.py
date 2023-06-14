from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page),
    path('category/<int:pk>', views.get_category_products),
    path('product/<str:name>/<int:pk>', views.get_exact_product),
    path('add-product-to-cart/<int:pk>', views.add_pr_to_cart),
    path('cart', views.user_cart),
    path('complete', views.complete_order),
    path('del_item/', views.delete_from_user_cart)
]

