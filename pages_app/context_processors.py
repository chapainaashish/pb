import json
from base import config
from .models import Navbar, Footer, Sidebar, Script
from list.models import Post, Category, Billboard
from filters.models import World, Country, Region, City, Facility, Service, Rating, SP1, SP2, SP3
from interests.models import Region as InterestRegion
from allauth.account.forms import LoginForm, SignupForm
from django.db.models import Subquery, Prefetch, Count


def split_array(arr, num_splits):
    avg_len = len(arr) // num_splits
    remainder = len(arr) % num_splits
    
    result = []
    index = 0
    
    for _ in range(num_splits):
        if remainder > 0:
            sub_array = arr[index : index + avg_len + 1]
            remainder -= 1
        else:
            sub_array = arr[index : index + avg_len]
        result.append(sub_array)
        index += len(sub_array)
    
    return result


def base_variable(request):
    # Filter Interest
    world_filters = World.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("order")
    country_filters = Country.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    region_filters = Region.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    city_filters = City.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    facility_filters = Facility.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    service_filters = Service.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    rating_filters = Rating.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("order")
    sp1_filters = SP1.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    sp2_filters = SP2.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")
    sp3_filters = SP3.objects.values("id", "name").annotate(count=Count("interests__id")).order_by("name")

    # Base
    header_script = Script.objects.get(name="HEADER SCRIPT")
    navbars = Navbar.objects.prefetch_related(
        "page",
        Prefetch('region', queryset=InterestRegion.objects.select_related('region_parent'))
    ).all().order_by("order")
    max_item = 10

    navbar_region = Navbar.objects.prefetch_related("region").filter(region__isnull=False).first()
    sorted_regions = navbar_region.region.all().order_by('navbar_order')
    regions = {}
    for lvl1 in sorted_regions:
        if lvl1.region_parent == None:
            regions_arr = []
            for lvl2 in sorted_regions:
                if lvl2.region_parent == lvl1:
                    regions_arr.append(lvl2)
                    for lvl3 in sorted_regions:
                        if lvl3.region_parent == lvl2:
                            regions_arr.append(lvl3)
            split_arrays = [[] for _ in range(5)]
            current_array = 0
            for item in regions_arr:
                if len(split_arrays[current_array]) >= max_item:
                    current_array += 1
                split_arrays[current_array].append(item)
            regions[lvl1] = split_arrays
    navbar_page = Navbar.objects.prefetch_related("page").filter(page__isnull=False).first()
    sorted_pages = navbar_page.page.all().order_by('navbar_order')
    pages = {}
    for lvl1 in sorted_pages:
        if lvl1.page_parent == None:
            pages_arr = []
            for lvl2 in sorted_pages:
                if lvl2.page_parent == lvl1:
                    pages_arr.append(lvl2)
                    for lvl3 in sorted_pages:
                        if lvl3.page_parent == lvl2:
                            pages_arr.append(lvl3)
            split_arrays = [[] for _ in range(5)]
            current_array = 0
            for item in pages_arr:
                if len(split_arrays[current_array]) >= max_item:
                    current_array += 1
                split_arrays[current_array].append(item)
            pages[lvl1] = split_arrays

    # sidebar
    sidebar = Sidebar.objects.get(id=1)
    default_sidebar = sidebar.sidebar
    default_ad_manager = sidebar.ad_manager

    # travel news
    travel_news = Post.objects.filter(category_id__in=Subquery(Category.objects.filter(slug="global-travel-news").values_list("id", flat=True))).order_by("-date_created")
    # billboards
    billboards = Billboard.objects.filter(display=True)

    # footer
    footer = list(Footer.objects.all().order_by("order"))
    footer_len = len(footer)
    remainder = int(footer_len % 3)
    item_per_col = int(footer_len /3)
    idx1 = item_per_col + remainder
    idx2 = idx1 + item_per_col
    footers1 = footer[:idx1]
    footers2 = footer[idx1:idx2]
    footers3 = footer[idx2:]
    return {"interest_label": config.INTEREST,
            "interest_label_capital": config.INTEREST.upper(),
            "domain": config.DOMAIN,
            "favicon": config.FAVICON,

            "info1_label": config.LABEL_INFO1,
            "info2_label": config.LABEL_INFO2,
            "info3_label": config.LABEL_INFO3,
            "info4_label": config.LABEL_INFO4,
            "info5_label": config.LABEL_INFO5,
            "long_info1_label": config.LABEL_LONG_INFO1,
            "web2_info_label": config.LABEL_WEB2_INFO,
            "submit_interest_slug": config.SUBMIT_INTEREST_SLUG,

            "activate_world": config.ACTIVATE_WORLD,
            "activate_country": config.ACTIVATE_COUNTRY,
            "activate_region": config.ACTIVATE_REGION,
            "activate_city": config.ACTIVATE_CITY,
            "activate_facility": config.ACTIVATE_FACILITY,
            "activate_service": config.ACTIVATE_SERVICE,
            "activate_rating": config.ACTIVATE_RATING,
            "activate_sp1": config.ACTIVATE_SP1,
            "activate_sp2": config.ACTIVATE_SP2,
            "activate_sp3": config.ACTIVATE_SP3,

            "world_filters": world_filters,
            "country_filters": country_filters,
            "region_filters": region_filters,
            "city_filters": city_filters,
            "facility_filters": facility_filters,
            "service_filters": service_filters,
            "rating_filters": rating_filters,
            "sp1_filters": sp1_filters,
            "sp2_filters": sp2_filters,
            "sp3_filters": sp3_filters,

            "world_text": config.WORLD_TEXT,
            "country_text": config.COUNTRY_TEXT,
            "region_text": config.REGION_TEXT,
            "city_text": config.CITY_TEXT,
            "facility_text": config.FACILITY_TEXT,
            "service_text": config.SERVICE_TEXT,
            "rating_text": config.RATING_TEXT,
            "sp1_text": config.SP1_TEXT,
            "sp2_text": config.SP2_TEXT,
            "sp3_text": config.SP3_TEXT,

            "world_icon": config.WORLD_ICON,
            "country_icon": config.COUNTRY_ICON,
            "region_icon": config.REGION_ICON,
            "city_icon": config.CITY_ICON,
            "facility_icon": config.FACILITY_ICON,
            "service_icon": config.SERVICE_ICON,
            "rating_icon": config.RATING_ICON,
            "sp1_icon": config.SP1_ICON,
            "sp2_icon": config.SP2_ICON,
            "sp3_icon": config.SP3_ICON,

            "header_script": header_script,
            "navbars": navbars,
            "sorted_regions": sorted_regions,
            "regions": regions,
            "sorted_pages": sorted_pages,
            "pages": pages,
            "default_sidebar": default_sidebar,
            "default_ad_manager": default_ad_manager,
            "travel_news": travel_news,
            "billboards": billboards,
            "footers1": footers1,
            "footers2": footers2,
            "footers3": footers3,

            'login_form': LoginForm(),
            'signup_form': SignupForm()
    }


def get_request_filter(request):
    filter_list = {
        "world": request.GET.get('world'),
        "country": request.GET.get('country'),
        "region": request.GET.get('region'),
        "city": request.GET.get('city'),
        "facility": request.GET.get('facility'),
        "service": request.GET.get('service'),
        "rating": request.GET.get('rating'),
        "sp1": request.GET.get('sp1'),
        "sp2": request.GET.get('sp2'),
        "sp3": request.GET.get('sp3'),
    }
    return json.dumps(filter_list)
