from django.shortcuts import render
from django.shortcuts import get_object_or_404
from main.models import Category, Project
from django.conf import settings
from .utils import get_template_for_lang


def page_404(request, exception=None):
    return render(request, "site/errors/404.html")


def page_500(request, exception=None):
    return render(request, "site/errors/500.html")


def index_page(request):
    return render(request, "site/index.html")


def about_page(request):
    return render(request, "site/header/about.html")


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


def service_page(request):
    return render(request, get_template_for_lang("site/service"))


def parts_page(request):
    return render(request, "site/parts.html")


def products_page(request):
    categories = None
    categories = Category.objects.all()
    return render(request, "site/products.html", context={"categories": categories})


def cart_page(request):
    return render(request, "site/cart.html")


def product_category(request, category_slug):
    if settings.CURRENT_SITE_LANG == "ru":
        category = get_object_or_404(Category, slug_ru=category_slug)
    else:
        category = get_object_or_404(Category, slug=category_slug)

    category_childs = None
    paginator = None

    return render(
        request,
        "site/catalog/product_category.html",
        context={
            "test": category,
            "category_childs": category_childs,
        },
    )
