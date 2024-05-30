import requests
import os
import html
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.core import files
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Autoblogging, Category, Billboard
from django.utils import timezone


def post_detail(request, category, post):
    post = get_object_or_404(Post, slug=post)

    # List Carousel
    list_carousel = Post.objects.filter(category__in=post.list_carousel.all()).order_by("-date_created")[:18]
    billboards = Billboard.objects.filter(display=True)

    context = {"post": post,
               "list_carousel": list_carousel,
               "billboards": billboards,
               }
    return render(request, "list/post.html", context)


def autoblogging(request):
    if request.user.is_superuser:
        sources = Autoblogging.objects.all()
        context = {"sources": sources}
        return render(request, "list/autoblogging.html", context)
    else:
        return HttpResponse("Sorry you are not allowed to access this page")


def pull_feeds(request, pk):
    if request.user.is_superuser:
        source = Autoblogging.objects.get(pk=pk)

        url = requests.get(source.url)
        soup = BeautifulSoup(url.content, "html.parser")
        length = source.items
        items = soup.find_all('item')[:length]
        contents = soup.find_all('content:encoded')[:length]

        for i in range(length-1, -1, -1):
            try:
                content = contents[i].text
                title = items[i].title.text
                body = content[content.find('</a>')+4:]
                category = Category.objects.get(pk=source.category.id)
                meta_keywords = title.lower()
                meta_description = html.unescape(
                    strip_tags(body[0:body.find(".")]))
                date_created = timezone.now()
            except:
                pass

            if not Post.objects.filter(title=title).exists():
                try:
                    post = Post(title=title,
                                body=body,
                                category=category,
                                meta_keywords=meta_keywords,
                                meta_description=meta_description,
                                date_created=date_created)
                except:
                    pass

                try:
                    link = content[content.find(
                        'src=')+5:content.find('alt')-2]
                    img_data = requests.get(link).content
                    with open('temp_image.jpg', 'wb') as handler:
                        handler.write(img_data)
                    with open('temp_image.jpg', 'rb') as handler:
                        file_name = link.split("/")[-1]
                        post.cover.save(file_name, files.File(handler))
                    os.remove("temp_image.jpg")
                except:
                    pass
        return redirect("news-autoblogging")
    else:
        return HttpResponse("Sorry you are not allowed to access this page")
