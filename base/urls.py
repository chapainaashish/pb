"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from base import config
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.http import Http404
from django.urls import path, include, re_path
from django.shortcuts import redirect
from multiurl import ContinueResolving, multiurl

from accounts.views import profile
from list.views import post_detail, autoblogging, pull_feeds
from pages_app.views import mainpage, footerpage, searchpage, page, listpage, postpage, linkup
from interests.views import interest_detail, interest_region, rr_form, edit_interest
from filters.views import filter_data, load_more_data

urlpatterns = [
    # wp sites
    re_path(r'^bangkok/.*$', lambda request: redirect('https://bangkok.top25restaurants.com/')),
    re_path(r'^phuket/.*$', lambda request: redirect('https://phuket.top25restaurants.com/')),
    re_path(r'^singapore/.*$', lambda request: redirect('https://singapore.top25restaurants.com/')),
    re_path(r'^hongkong/.*$', lambda request: redirect('https://hongkong.top25restaurants.com/')),
    re_path(r'^shanghai/.*$', lambda request: redirect('https://shanghai.top25restaurants.com/')),
    re_path(r'^delhi/.*$', lambda request: redirect('https://delhi.top25restaurants.com/')),

    # admin
    path('admin/', admin.site.urls),

    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # filters
    path('filter-data/', filter_data, name='filter-data'),
    path('load-more-data/', load_more_data, name='load-more-data'),

    # accounts
    path('', include('allauth.urls')),
    path('profile/', profile, name='profile'),

    # list
    path('news/autoblogging/', autoblogging, name='news-autoblogging'),
    path('pull/<int:pk>/', pull_feeds, name='news-pull'),

    # pages_app
    path('', mainpage, name='mainpage'),
    path('search/', searchpage, name='searchpage'),
    multiurl(
        path('<slug:slug>/', footerpage, name='footerpage'),
        path('<str:region>/', interest_region, name="region-without-parent"),
        path('<slug:slug>/', listpage, name='listpage'),
        path('<slug:slug>/', postpage, name='postpage'),
        catch = (Http404, ContinueResolving)
    ),
    path('explore/<slug:slug>/', page, name='page'),
    path('social/<slug:slug>/', linkup, name='linkup'),

    # interests
    path(config.EDIT_INTEREST_PATH, edit_interest, name="edit-interest"),
    path(config.INTEREST_REVIEW_PATH, rr_form, name="interest-review"),
    path(config.INTEREST_WITHOUT_PARENT_REVIEW_PATH, rr_form, name="interest-without-parent-review"),
    path(config.INTEREST_DETAIL_PATH, interest_detail, name="interest-detail"),
    path(config.INTEREST_DETAIL_WITHOUT_PARENT_PATH, interest_detail, name="interest-detail-without-parent"),

    multiurl(
        path('<str:parent>/<str:region>/', interest_region, name="region"),
        path('<slug:category>/<slug:post>/', post_detail, name='post-detail'),
        catch = (Http404, ContinueResolving)
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error Page
handler400 = 'pages_app.views.bad_request_view'
handler403 = 'pages_app.views.permission_denied_view'
handler404 = 'pages_app.views.page_not_found_view'
handler500 = 'pages_app.views.server_error_view'
