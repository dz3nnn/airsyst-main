from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_page, name="index-page"),
    # Errors
    path("404/", views.page_404, name="error-404"),
    path("500/", views.page_500, name="error-500"),
    # Profile
    path("profile/", views.profile_view, name="profile-page"),
    path("history/", views.history_view, name="history-page"),
    path("forgot/", views.forgot_view, name="forgot-page"),
    path("login/", views.login_view, name="login-page"),
    path("register/", views.register_view, name="register-page"),
    path("logout/", views.logout_view, name="logout"),
    # Header
    path("about/", views.about_page, name="about-page"),
    path("contacts/", views.contacts_page, name="contacts-page"),
    path("projects/", views.projects_page, name="projects-page"),
    path(
        "project/<int:project_id>/",
        views.project_single_page,
        name="project-single-page",
    ),
    path("cart/", views.cart_page, name="cart-page"),
    # Main pages
    path("service/", views.service_page, name="service-page"),
    path("parts/", views.parts_page, name="parts-page"),
    path("products/", views.products_page, name="products-page"),
    path(
        "products/<slug:category_slug>/",
        views.product_category,
        name="product-category-by-slug",
    ),
    path(
        "products/catalog/<slug:category_slug>/",
        views.product_catalog_view,
        name="product-catalog-by-slug",
    ),
    path(
        "product/<slug:product_article>/",
        views.product_card_view,
        name="product-card-by-article",
    ),
    # Requests
    path("send_feedback/", views.send_feedback_view, name="send-feedback"),
    path("search/", views.search_view, name="search-request"),
]
