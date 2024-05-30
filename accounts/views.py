from base import config
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from pages_app.models import ContentPage
from interests.models import ReviewAndRating, Interest
from interests.forms import CommentForm
from datetime import date, timedelta


@login_required
def profile(request):
    # From contact_us
    if 'contact_us' in request.session:
        request.session.pop('contact_us')
        return redirect("footerpage", slug="contact-us")
    
    # From submit_interest
    if 'submit_interest' in request.session:
        request.session.pop('submit_interest')
        return redirect("footerpage", slug=config.SUBMIT_INTEREST_SLUG)

    user = request.user
    profile = Profile.objects.get(user=user)
    interests = Interest.objects.filter(user=user)
    rr_received = ReviewAndRating.objects.filter(interest__in=interests)

    # Profile Form
    form = ProfileForm(instance=profile)
    review_and_rating = ReviewAndRating.objects.filter(
        user=user, approved=True)
    if request.method == 'POST' and 'profile_form' in request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")

    # Comment Form
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid() and 'comment_form' in request.POST:
        rr = ReviewAndRating.objects.get(pk=request.POST['rr_id'])
        instance = comment_form.save(commit=False)
        instance.user = request.user
        instance.rr = rr
        instance.save()
        return redirect("profile")

    content_page = get_object_or_404(ContentPage, types="SEARCH_PAGE")
    context = {
        'user': user,
        'profile': profile,
        'content_page': content_page,
        'form': form,
        'review_and_rating': review_and_rating,
        'interests': interests,
        'rr_received': rr_received,
        'comment_form': comment_form,
    }
    return render(request, "account/profile.html", context)
