from django.shortcuts import render, get_object_or_404
from main.models import Category, Project, Brand
from django.conf import settings
from .utils import get_template_for_lang
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Errors
def page_404(request, exception=None):
    return render(request, "site/errors/404.html")


def page_500(request, exception=None):
    return render(request, "site/errors/500.html")


# Profile
@login_required(login_url="/login/")
def profile_view(request):
    return render(request, "profile/profile-page.html")


@login_required(login_url="/login/")
def history_view(request):
    return render(request, "profile/history-page.html")


def logout_view(request):
    logout(request)
    return redirect(login_view)


def forgot_view(request):
    return render(request, "profile/forgot.html")


def login_view(request):
    error_message = None
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect("profile_view")
        else:
            error_message = _("Invalid login")
    return render(request, "profile/auth.html", {"error_message": error_message})


def register_view(request):
    error_message = None
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user_exists = User.objects.filter(username=username)
        if not user_exists:
            user = User.objects.create_user(username, username, password)
            redirect(login_view)
        else:
            error_message = _("User already registered")
    return render(request, "profile/register.html", {"error_message": error_message})


# Main
def index_page(request):
    return render(request, "site/index.html")


def about_page(request):
    return render(request, "site/header/about.html")


def service_page(request):
    return render(request, get_template_for_lang("site/service"))


def cart_page(request):
    return render(request, "site/cart.html")


# Projects
def projects_page(request):
    page_filter = request.GET.get("filter")
    if page_filter:
        projects = Project.objects.filter(project_type=page_filter)
    else:
        projects = Project.objects.all()
    return render(request, "site/header/projects.html", context={"projects": projects})


def project_single_page(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(
        request,
        "site/project-single.html",
        context={"project": project, "images": project.get_all_images},
    )


# Parts
def parts_page(request):
    all_brands = Brand.objects.all()
    return render(request, "site/parts.html", {"all_brands": all_brands})


# Equipment
def products_page(request):
    categories = Category.objects.filter(parent=None)
    return render(request, "site/products.html", context={"categories": categories})


def product_category(request, category_slug):
    if settings.CURRENT_SITE_LANG == "ru":
        category = get_object_or_404(Category, slug_ru=category_slug)
    else:
        category = get_object_or_404(Category, slug=category_slug)

    category_childs = category.get_children()
    paginator = None

    return render(
        request,
        "site/catalog/product_category.html",
        context={
            "test": category,
            "category": category,
            "category_childs": category_childs,
        },
    )


def product_catalog_view(request, category_slug):
    if settings.CURRENT_SITE_LANG == "ru":
        category = get_object_or_404(Category, slug_ru=category_slug)
    else:
        category = get_object_or_404(Category, slug=category_slug)

    return render(request, "site/catalog/product_catalog.html", {"category": category})
