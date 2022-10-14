from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index-page'),

    # Errors
    path('404/', views.page_404, name='error-404'),
    path('500/', views.page_500, name='error-500'),

    # Header
    path('about/', views.about_page, name='about-page'),
    path('projects/', views.projects_page, name='projects-page'),
    path('cart/', views.cart_page, name='cart-page'),

    # Main pages
    path('service/', views.service_page, name='service-page'),
    path('parts/', views.parts_page, name='parts-page'),
    path('products/', views.products_page, name='products-page'),

    path('products/<slug:category_slug>/',
         views.product_category, name='product-category-by-slug')
]
