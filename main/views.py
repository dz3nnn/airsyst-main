from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.core.paginator import Paginator

from main.models import (
    Category,
    Equipment_Item,
    Option,
    OptionRelation,
    Project,
    Brand,
    Slider,
)
from main.helps import apply_filter_for_equip
from main.utils import get_template_for_lang, message_to_managers
from main.filters import get_equipment_brands, get_certificates_for_current_lang

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
        username = request.POST.get("username")
        password = request.POST.get("password")
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
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_exists = User.objects.filter(username=username)
        if not user_exists:
            user = User.objects.create_user(username, username, password)
            redirect(login_view)
        else:
            error_message = _("User already registered")
    return render(request, "profile/register.html", {"error_message": error_message})


# Main
def index_page(request):
    all_brands = Brand.objects.all()
    equip_brands = get_equipment_brands()
    context = {
        "all_brands": all_brands,
        "equip_brands": equip_brands,
        "sliders": Slider.objects.all(),
    }
    return render(
        request,
        "site/index.html",
        context,
    )


def about_page(request):
    return render(request, "site/header/about.html")


def dealers_view(request):
    return render(request, "site/header/dealers.html")


def contacts_page(request):
    return render(request, "site/header/contacts.html")


def certificates_view(request):
    certificates = get_certificates_for_current_lang()
    context = {"certificates": certificates}
    return render(request, "site/header/certificates.html", context)


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
    categories = Category.objects.filter(parent=None).order_by("name")
    return render(request, "site/products.html", context={"categories": categories})


def product_category(request, category_slug):
    if settings.CURRENT_SITE_LANG == "ru":
        category = get_object_or_404(Category, slug_ru=category_slug)
    else:
        category = get_object_or_404(Category, slug=category_slug)

    category_childs = category.get_children()

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

    items = Equipment_Item.objects.filter(category=category)
    items_pk = items.values_list("pk", flat=True)
    relations = OptionRelation.objects.filter(equipment__pk__in=items_pk).values_list(
        "option__pk", flat=True
    )
    options = Option.objects.filter(pk__in=relations)

    filtered_items = apply_filter_for_equip(request, items)

    paginator = Paginator(filtered_items, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
        "items": items,
        "brands": Brand.objects.all(),
        "options": options,
    }
    return render(
        request,
        "site/catalog/product_catalog.html",
        context,
    )


def product_card_view(request, product_article):
    product = get_object_or_404(Equipment_Item, article=product_article)
    assert product is not None

    return render(
        request,
        "site/catalog/product_card.html",
        {"item": product},
    )


# Requests
def send_feedback_view(request):
    if request.POST:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if phone or email:
            message_to_managers()
            JsonResponse({"success": "true"})

    return JsonResponse({"success": "false"})


def search_view(request):
    def _parse_product(eq_item: Equipment_Item):
        return {
            "image": eq_item.get_first_image_url,
            "name": eq_item.name,
            "article": eq_item.article,
            "price": eq_item.get_final_price,
            "link": eq_item.get_absolute_url(),
        }

    search = request.GET.get("q")
    result = []
    if search:
        # Products
        for item in Equipment_Item.objects.all():
            result.append(_parse_product(item))
    return JsonResponse({"items": result})
