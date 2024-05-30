from base import config
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.cache import cache
from django.core.mail import send_mail

from pages_app.context_processors import get_request_filter
from .models import ContentPage, ImageUpload
from interests.models import Interest, Region
from interests.forms import InterestForm
from list.models import Post, Category, Billboard

from mailing.models import ContactEntry, Subscriber
from mailing.forms import ContactEntryForm, SubscriberForm

from itertools import chain


def bad_request_view(request, exception):
    return render(request, 'pages_app/400.html', status=400)


def permission_denied_view(request, exception):
    return render(request, 'pages_app/403.html', status=403)


def page_not_found_view(request, exception):
    return render(request, 'pages_app/404.html', status=404)


def server_error_view(request):
    return render(request, 'pages_app/500.html', status=500)


def mainpage(request):
    content_page = get_object_or_404(ContentPage, types="HOME_PAGE")
    image_carousel = ImageUpload.objects.filter(page=content_page)

    # List Section 1: Interests
    page_type = content_page.geo_filters
    interests_qs = Interest.objects.select_related("region__region_parent").filter(regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 2: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page2')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.select_related("category").filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    context = {"content_page": content_page,
               "image_carousel": image_carousel,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    # Popup message if the form is submitted successfully
    if("contact_form_msg" in request.session):
        context["msg"] = request.session["contact_form_msg"]
        request.session.pop("contact_form_msg")
    if("subscribe_form_msg" in request.session):
        context["msg"] = request.session["subscribe_form_msg"]
        request.session.pop("subscribe_form_msg")
    if("interest_form_msg" in request.session):
        context["msg"] = request.session["interest_form_msg"]
        request.session.pop("interest_form_msg")
    if("send_email_form_msg" in request.session):
        context["msg"] = request.session["send_email_form_msg"]
        request.session.pop("send_email_form_msg")
    return render(request, "pages_app/main_page.html", context)


def footerpage(request, slug):
    content_page = get_object_or_404(ContentPage, slug=slug, types="FOOTER")
    contact_entry_form = ContactEntryForm()
    subscriber_form = SubscriberForm()
    interest_form = InterestForm()

    # List Section 1: Interests
    page_type = content_page.geo_filters
    interests_qs = Interest.objects.filter(regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    # Set Cache
    # cache.set("page_type", page_type)
    # cache.set("defaultInterests", interests_qs)
    # cache.set("currentInterests", interests_qs)
    # cache.set("perPage", per_page)
    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 2: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page2')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    error_msg = None
    if slug == "contact-us":
        contact_entry_form = ContactEntryForm()
        if request.user.is_authenticated:
            if request.method == "POST":
                contact_entry_form = ContactEntryForm(request.POST)
                if contact_entry_form.is_valid():
                    name = contact_entry_form.cleaned_data["name"]
                    email = contact_entry_form.cleaned_data["email"]
                    subject = contact_entry_form.cleaned_data["subject"]
                    message = contact_entry_form.cleaned_data["message"]
                    ContactEntry.objects.create(name=name, email=email, subject=subject, message=message)
                    send_mail(subject,
                        "From: " + name + 
                        "\nEmail: " + email + 
                        "\n\n" + message,
                        '',
                        [config.DEFAULT_TO_EMAIL]
                    )
                    request.session["contact_form_msg"] = "Your message has been sent! Thank you!"
                    return redirect("mainpage")
        else:
            request.session["contact_us"] = True
            return redirect("account_login")

    elif slug == "newsletter":
        subscriber_form = SubscriberForm()
        if request.method == "POST":
            subscriber_form = SubscriberForm(request.POST)
            if subscriber_form.is_valid():
                Subscriber.objects.create(
                    name = subscriber_form.cleaned_data["name"],
                    email = subscriber_form.cleaned_data["email"],
                    country = subscriber_form.cleaned_data["country"])
                request.session["subscribe_form_msg"] = "Thanks for subscribing to our newsletter!"
                return redirect("mainpage")

    elif slug == config.SUBMIT_INTEREST_SLUG:
        interest_form = InterestForm()
        if request.user.is_authenticated:
            if request.method == "POST":
                interest_form = InterestForm(request.POST, request.FILES)
                if interest_form.is_valid():
                    instance = interest_form.save(commit=False)
                    instance.user = request.user
                    instance.email1 = request.user.email
                    instance.isvalidated = False
                    instance.save()
                    interest_form.save_m2m()
                    request.session["interest_form_msg"] = "Your " + config.INTEREST.lower() + " has been successfully submitted!"
                    return redirect("mainpage")
                else:
                    error_msg = "Please check the information entered, some items require your attention."
        else:
            request.session["submit_interest"] = True
            return redirect("account_login")

    context = {"content_page": content_page,
               "contact_entry_form": contact_entry_form,
               "subscriber_form": subscriber_form,
               "interest_form": interest_form,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               "error_msg": error_msg,
               }
    return render(request, "pages_app/footer_page.html", context)


def searchpage(request):
    content_page = get_object_or_404(ContentPage, types="SEARCH_PAGE")

    # List Section 1: Search Result
    if request.method == "POST":
        searched = request.POST['searched']
    else:
        searched = request.GET.get('searched')
    interest = Interest.objects.filter(
        Q(name__icontains=searched) |
        Q(text__icontains=searched) |
        Q(info1__icontains=searched) |
        Q(info2__icontains=searched) |
        Q(info5__icontains=searched) |
        Q(linkup_tags__icontains=searched) |
        Q(meta_description__icontains=searched) |
        Q(meta_keywords__icontains=searched) |
        Q(slug__icontains=searched)
    ).order_by("-rating")
    regions = Region.objects.filter(
        Q(name__icontains=searched) |
        Q(title__icontains=searched) |
        Q(description__icontains=searched) |
        Q(meta_description__icontains=searched) |
        Q(meta_keywords__icontains=searched)
    )
    pages = ContentPage.objects.filter(
        Q(content__icontains=searched) |
        Q(additional_content__icontains=searched) |
        Q(meta_description__icontains=searched) |
        Q(meta_keywords__icontains=searched)
    )
    post = Post.objects.filter(
        Q(title__icontains=searched) |
        Q(body__icontains=searched) |
        Q(tags__name__icontains=searched) |
        Q(meta_description__icontains=searched) |
        Q(meta_keywords__icontains=searched)
    ).distinct().order_by("-date_created")
    # wine_post = post.filter(category__name__contains=["Best Wine Clubs", "Wine Tasting", "Wine News"])
    # all_post = post.exclude(category__name__contains=["Best Wine Clubs", "Wine Tasting", "Wine News", "Global Travel News"])
    # news_post = post.filter(category__name__contains="Global Travel News")

    result_list = list(chain(interest, regions, pages, post))
    p = Paginator(result_list, 10)
    page = request.GET.get('page1')
    results = p.get_page(page)

    # List Section 2: Interests
    page_type = content_page.geo_filters
    interests_qs = Interest.objects.filter(regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    # Set Cache
    # cache.set("page_type", page_type)
    # cache.set("defaultInterests", interests_qs)
    # cache.set("currentInterests", interests_qs)
    # cache.set("perPage", per_page)
    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 3: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page3')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    context = {"content_page": content_page,
               "searched": searched,
               "results": results,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "pages_app/search_page.html", context)


def page(request, slug):
    content_page = get_object_or_404(ContentPage, slug=slug, types__in=["PAGE", "WITHOUT_SIDEBAR"])
    image_carousel = ImageUpload.objects.filter(page=content_page)

    # List Section 1: Interests
    page_type = content_page.geo_filters
    interests_qs = Interest.objects.filter(regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    # Set Cache
    # cache.set("page_type", page_type)
    # cache.set("defaultInterests", interests_qs)
    # cache.set("currentInterests", interests_qs)
    # cache.set("perPage", per_page)
    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 2: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page2')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    context = {"content_page": content_page,
               "image_carousel": image_carousel,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "pages_app/page.html", context)


def listpage(request, slug):
    content_page = get_object_or_404(ContentPage, slug=slug, types="LIST")
    image_carousel = ImageUpload.objects.filter(page=content_page)

    # List Section 1: Main List Section
    content_pages = ContentPage.objects.filter(page_parent=content_page)
    p = Paginator(content_pages, 10)
    page = request.GET.get('page1')
    main_list = p.get_page(page)

    # List Section 2: Interests
    page_type = content_page.geo_filters
    interests_qs = Interest.objects.filter(regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    # Set Cache
    # cache.set("page_type", page_type)
    # cache.set("defaultInterests", interests_qs)
    # cache.set("currentInterests", interests_qs)
    # cache.set("perPage", per_page)
    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 3: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page3')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)
    context = {"content_page": content_page,
               "image_carousel": image_carousel,
               "main_list": main_list,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "pages_app/list_page.html", context)


def postpage(request, slug):
    content_page = get_object_or_404(ContentPage, slug=slug, types="POST")
    image_carousel = ImageUpload.objects.filter(page=content_page)

    # List Section 1: Main Post Section
    category = Category.objects.get(slug=content_page.slug)
    p = Paginator(Post.objects.filter(category=category).order_by("-date_created"), 10)
    page = request.GET.get('page1')
    main_list = p.get_page(page)

    # List Section 2: Interests
    page_type = content_page.geo_filters
    interests_qs = Interest.objects.filter(regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    # Set Cache
    # cache.set("page_type", page_type)
    # cache.set("defaultInterests", interests_qs)
    # cache.set("currentInterests", interests_qs)
    # cache.set("perPage", per_page)
    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 3: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page3')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)
    context = {"content_page": content_page,
               "image_carousel": image_carousel,
               "main_list": main_list,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "pages_app/post_page.html", context)


def linkup(request, slug):
    content_page = get_object_or_404(ContentPage, slug=slug, types="LINKUP")
    image_carousel = ImageUpload.objects.filter(page=content_page)

    # List Section 1: Interests
    slug = slug.replace("-", " ")
    page_type = content_page.geo_filters
    regex = r'(?:^|(?<=,\s))' + slug + r'(?:(?=,)|$)'
    interests_qs = Interest.objects.filter(linkup_tags__regex=regex, regions__in=content_page.category.all(), display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    filter_list = get_request_filter(request)

    # Pagination
    per_page = 10
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]
    interests = interests_qs[:per_page]

    # Set Cache
    # cache.set("page_type", page_type)
    # cache.set("defaultInterests", interests_qs)
    # cache.set("currentInterests", interests_qs)
    # cache.set("perPage", per_page)
    interests_id = list(interests_qs.values_list('id', flat=True))

    # List Section 2: List Section
    p = Paginator(Post.objects.filter(category__in=content_page.list_section.all()).order_by("-date_created"), 10)
    page = request.GET.get('page2')
    list_section = p.get_page(page)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=content_page.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    context = {"content_page": content_page,
               "image_carousel": image_carousel,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_section": list_section,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "pages_app/page.html", context)
