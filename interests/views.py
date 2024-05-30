from base import config
from django.shortcuts import render, get_object_or_404, redirect
from pages_app.context_processors import get_request_filter
from .models import Interest, Region, RegionImage, TopSliderImage, CoverSliderImage, ReviewAndRating, Comment
from .forms import ReviewRatingForm, InterestForm, EmailInterestForm
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from list.models import Post, Category, Billboard


def interest_detail(request, region, slug, parent=None):
    interest = get_object_or_404(Interest, slug=slug, display=True)
    comments = Comment.objects.filter(approved=True)
    yard_images = TopSliderImage.objects.filter(interest=interest)
    yard_cover_images = CoverSliderImage.objects.filter(interest=interest)
    review_and_rating = ReviewAndRating.objects.filter(
        interest=interest, approved=True)
    recent_reviews = ReviewAndRating.objects.filter(
        interest=interest, approved=True).order_by('-id')[:3]
    form = EmailInterestForm()
    if request.user.is_authenticated:
        if request.method == "POST":
            send_email_form = EmailInterestForm(request.POST)
            if send_email_form.is_valid():
                name = send_email_form.cleaned_data["name"],
                email = send_email_form.cleaned_data["email"],
                subject = send_email_form.cleaned_data["subject"],
                message = send_email_form.cleaned_data["message"]
                body = "From: " + name[0] + " - " + email[0] + "\n" + message
                send_mail(subject[0], body, "", [interest.email1, interest.email2])
                request.session["send_email_form_msg"] = "Your message has been successfully sent!"
                return redirect("mainpage")

    # List Carousel
    list_carousel = Post.objects.filter(category__in=interest.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    error_msg = None
    success_msg = None
    if "rr_form_error_msg" in request.session:
        error_msg = request.session["rr_form_error_msg"]
        request.session.pop("rr_form_error_msg")
    elif "rr_form_success_msg" in request.session:
        success_msg = request.session["rr_form_success_msg"]
        request.session.pop("rr_form_success_msg")
    context = {"interest": interest,
               "yard_images": yard_images,
               "yard_cover_images": yard_cover_images,
               "review_and_rating": review_and_rating,
               "comments": comments,
               "recent_reviews": recent_reviews,
               "error_msg": error_msg,
               "success_msg": success_msg,
               "list_carousel": list_carousel,
               "billboards": billboards,
               "form": form,
               }
    return render(request, "interests/interest.html", context)


def interest_region(request, region, parent=None):
    region = get_object_or_404(Region, slug=region)
    region_images = RegionImage.objects.filter(region=region)

    # List Section 1: Interest By Region
    page_type = region.geo_filters
    interests_qs = Interest.objects.filter(regions=region, display=True).distinct().order_by("-rating")
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

    # List Carousel
    list_carousel = Post.objects.filter(category__in=region.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    context = {"region": region,
               "region_images": region_images,
               "page_type": page_type,
               "interests": interests,
               "interests_id": interests_id,
               "total_interests": total_interests,
               "filter_list": filter_list,
               "per_page": per_page,
               "num_pages": num_pages,
               "current_page": current_page,
               "page_range": page_range,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "interests/interest_region.html", context)


@login_required
def rr_form(request, region, slug, parent=None):
    interest = get_object_or_404(Interest, slug=slug)
    yard_images = TopSliderImage.objects.filter(interest=interest)
    yard_cover_images = CoverSliderImage.objects.filter(interest=interest)
    recent_reviews = ReviewAndRating.objects.filter(
        interest=interest, approved=True).order_by('-id')[:3]
    form = ReviewRatingForm(request.POST or None)

    # List Carousel: Global Travel News
    category = Category.objects.get(slug="global-travel-news")
    travel_news = Post.objects.filter(category=category).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    # Check if there is a previous review
    try:
        obj = ReviewAndRating.objects.filter(
            user=request.user, interest=interest).latest('date_created')
        wait = obj.date_created.date() + timedelta(days=10)
        if date.today() < wait:
            allowed = False
        else:
            allowed = True
    except:
        allowed = True

    error_msg = None
    if request.method == "POST":
        form = ReviewRatingForm(request.POST)
        if form.is_valid():
            if not allowed:
                request.session['rr_form_error_msg'] = "Sorry you can't post right now. You have to wait 10 days since the last post."
            else:
                if request.user.is_authenticated:
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.interest = interest
                    instance.save()
                    request.session['rr_form_success_msg'] = "Your Rating and Review has been submitted. Thank you."
            return redirect(interest.get_absolute_url())
        else:
            error_msg = "Please check the information entered, some items require your attention."

    context = {"interest": interest,
               "yard_images": yard_images,
               "yard_cover_images": yard_cover_images,
               "recent_reviews": recent_reviews,
               "form": form,
               "rr_form_label1": config.LABEL_RR_FORM1,
               "rr_form_label2": config.LABEL_RR_FORM2,
               "rr_form_label3": config.LABEL_RR_FORM3,
               "rr_form_label4": config.LABEL_RR_FORM4,
               "rr_form_label5": config.LABEL_RR_FORM5,
               "rr_form_label6": config.LABEL_RR_FORM6,
               "travel_news": travel_news,
               "billboards": billboards,
               "error_msg": error_msg
               }
    return render(request, "interests/rr_form.html", context)


def edit_interest(request, interest):
    interest = get_object_or_404(Interest, slug=interest)

    # List Carousel: Global Travel News
    category = Category.objects.get(slug="global-travel-news")
    travel_news = Post.objects.filter(category=category).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    if interest.user == request.user:
        interest_form = InterestForm(instance=interest)
        if request.user.is_authenticated:
            if request.method == "POST":
                interest_form = InterestForm(request.POST, request.FILES, instance=interest)
                if interest_form.is_valid():
                    instance = interest_form.save(commit=False)
                    instance.display = False
                    instance.send_mail = False
                    instance.save()
                    interest_form.save_m2m()
                    # From Admin to User
                    subject = "Update " + config.INTEREST
                    body = "Your " + config.INTEREST.lower() + " updates have been recorded but have to be approved by Admin."
                    send_mail(subject, body, "", [interest.email1])
                    # From User to Admin
                    subject = "Update " + config.INTEREST
                    body = "Update " + config.INTEREST + " from User"
                    send_mail(subject, body, "", [config.DEFAULT_TO_EMAIL])
                    return redirect("mainpage")
    else:
        return redirect("mainpage")
    context = {"interest": interest,
                "interest_form": interest_form,
                "travel_news": travel_news,
                "billboards": billboards,
                }
    return render(request, "interests/edit_interest.html", context)
