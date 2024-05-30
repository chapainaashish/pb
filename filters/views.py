from base import config
from django.http import JsonResponse
from django.template.loader import render_to_string
from interests.models import Interest
from .models import World, Country, Region, City, Facility, Service, Rating, SP1, SP2, SP3
from django.db.models import Count


def filter_interests(param_dict):
    interestList = param_dict["interestList"]

    if len(param_dict["world"]) > 0:
        interestList = interestList.filter(world_filter__in=param_dict["world"])

    if len(param_dict["country"]) > 0:
        interestList = interestList.filter(country_filter__in=param_dict["country"])

    if len(param_dict["region"]) > 0:
        interestList = interestList.filter(region_filter__in=param_dict["region"])

    if len(param_dict["city"]) > 0:
        interestList = interestList.filter(city_filter__in=param_dict["city"])

    if len(param_dict["facility"]) > 0:
        interestList = interestList.filter(facility_filter__in=param_dict["facility"])

    if len(param_dict["service"]) > 0:
        interestList = interestList.filter(service_filter__in=param_dict["service"])

    if len(param_dict["rating"]) > 0:
        interestList = interestList.filter(rating_filter__in=param_dict["rating"])

    if len(param_dict["sp1"]) > 0:
        interestList = interestList.filter(sp1_filter__in=param_dict["sp1"])

    if len(param_dict["sp2"]) > 0:
        interestList = interestList.filter(sp2_filter__in=param_dict["sp2"])

    if len(param_dict["sp3"]) > 0:
        interestList = interestList.filter(sp3_filter__in=param_dict["sp3"])

    interests_qs = interestList.filter(display=True).distinct()

    return interests_qs


def prepare_filter(param_dict) -> dict:
    ft = dict()
    if len(param_dict["world"]) > 0:
        ft.update(world_filter__in=param_dict["world"])

    if len(param_dict["country"]) > 0:
        ft.update(country_filter__in=param_dict["country"])

    if len(param_dict["region"]) > 0:
        ft.update(region_filter__in=param_dict["region"])

    if len(param_dict["city"]) > 0:
        ft.update(city_filter__in=param_dict["city"])

    if len(param_dict["facility"]) > 0:
        ft.update(facility_filter__in=param_dict["facility"])

    if len(param_dict["service"]) > 0:
        ft.update(service_filter__in=param_dict["service"])

    if len(param_dict["rating"]) > 0:
        ft.update(rating_filter__in=param_dict["rating"])

    if len(param_dict["sp1"]) > 0:
        ft.update(sp1_filter__in=param_dict["sp1"])

    if len(param_dict["sp2"]) > 0:
        ft.update(sp2_filter__in=param_dict["sp2"])

    if len(param_dict["sp3"]) > 0:
        ft.update(sp3_filter__in=param_dict["sp3"])

    return ft


def filter_data(request):
    # page_type = cache.get('page_type')
    page_type = request.GET.get('pageType')
    defaultInterests = request.GET.get('defaultInterests')
    defaultInterests = defaultInterests.strip('][').split(', ')

    initial_dict = {
        # "interestList": cache.get('defaultInterests'),
        "interestList": Interest.objects.filter(id__in=defaultInterests),
        "world": request.GET.getlist('world[]'),
        "country": request.GET.getlist('country[]'),
        "region": request.GET.getlist('region[]'),
        "city": request.GET.getlist('city[]'),
        "facility": request.GET.getlist('facility[]'),
        "service": request.GET.getlist('service[]'),
        "rating": request.GET.getlist('rating[]'),
        "sp1": request.GET.getlist('sp1[]'),
        "sp2": request.GET.getlist('sp2[]'),
        "sp3": request.GET.getlist('sp3[]'),
    }

    interests_qs = filter_interests(initial_dict).order_by("-rating")
    total_interests = filter_interests(initial_dict).count()
    interests_id = list(interests_qs.values_list('id', flat=True))

    # Pagination
    # per_page = int(cache.get('perPage'))
    per_page = int(request.GET.get('perPage'))
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = 1
    page_range = [i for i in range(1, num_pages + 1)]

    interests = interests_qs[((current_page-1)*per_page):(current_page*per_page)]

    world = World.objects.prefetch_related("interests").all().order_by("order")
    country = Country.objects.prefetch_related("interests").all().order_by("name")
    region = Region.objects.prefetch_related("interests").all().order_by("name")
    city = City.objects.prefetch_related("interests").all().order_by("name")
    facility = Facility.objects.prefetch_related("interests").all().order_by("name")
    service = Service.objects.prefetch_related("interests").all().order_by("name")
    rating = Rating.objects.prefetch_related("interests").all().order_by("order")
    sp1 = SP1.objects.prefetch_related("interests").all().order_by("name")
    sp2 = SP2.objects.prefetch_related("interests").all().order_by("name")
    sp3 = SP3.objects.prefetch_related("interests").all().order_by("name")

    interestList = initial_dict.get("interestList", [])
    count_list = []

    rating_ids = [r.id for r in rating]
    rating_ft = prepare_filter(initial_dict.copy())
    rating_ft.update(rating_filter__in=rating_ids, display=True)
    interest_ratings = interestList.filter(**rating_ft).values("rating_filter__id").annotate(
        total=Count("rating_filter__id"))
    interest_ratings_mapping = dict()
    [interest_ratings_mapping.update({interest_rating.get("rating_filter__id"): interest_rating.get("total", 0)}) for
     interest_rating in interest_ratings]
    for rating_id in rating_ids:
        count_list.append(interest_ratings_mapping.get(rating_id, 0))

    if page_type == "WORLD":
        world_ids = [w.id for w in world]
        world_ft = prepare_filter(initial_dict.copy())
        world_ft.update(world_filter__in=world_ids, display=True)
        interest_worlds = interestList.filter(**world_ft).values("world_filter__id").annotate(
            total=Count("world_filter__id"))
        interest_worlds_mapping = dict()
        [interest_worlds_mapping.update({interest_world.get("world_filter__id"): interest_world.get("total", 0)}) for
         interest_world in interest_worlds]
        for world_id in world_ids:
            count_list.append(interest_worlds_mapping.get(world_id, 0))

    if page_type == "WORLD" or page_type == "COUNTRY":
        country_ids = [c.id for c in country]
        country_ft = prepare_filter(initial_dict.copy())
        country_ft.update(country_filter__in=country_ids, display=True)
        interest_countries = interestList.filter(**country_ft).values("country_filter__id").annotate(
            total=Count("country_filter__id"))
        interest_countries_mapping = dict()
        [interest_countries_mapping.update({interest_country.get("country_filter__id"): interest_country.get("total", 0)}) for interest_country in interest_countries]
        for country in country_ids:
            count_list.append(interest_countries_mapping.get(country, 0))

    if page_type == "WORLD" or page_type == "COUNTRY" or page_type == "REGION":
        region_ids = [r.id for r in region]
        region_ft = prepare_filter(initial_dict.copy())
        region_ft.update(region_filter__in=region_ids, display=True)
        interest_regions = interestList.filter(**region_ft).values("region_filter__id").annotate(
            total=Count("region_filter__id"))
        interest_regions_mapping = dict()
        [interest_regions_mapping.update({interest_region.get("region_filter__id"): interest_region.get("total", 0)}) for interest_region in interest_regions]
        for region_id in region_ids:
            count_list.append(interest_regions_mapping.get(region_id, 0))

    if page_type == "WORLD" or page_type == "COUNTRY" or page_type == "REGION" or page_type == "CITY":
        city_ids = [c.id for c in city]
        city_ft = prepare_filter(initial_dict.copy())
        city_ft.update(city_filter__in=city_ids, display=True)
        interest_cities = interestList.filter(**city_ft).values("city_filter__id").annotate(total=Count("city_filter__id"))
        interest_cities_mapping = dict()
        [interest_cities_mapping.update({interest_city.get("city_filter__id"): interest_city.get("total", 0)}) for interest_city in interest_cities]
        for city_id in city_ids:
            count_list.append(interest_cities_mapping.get(city_id, 0))

    sp1_ids = [sp.id for sp in sp1]
    sp1_ft = prepare_filter(initial_dict.copy())
    sp1_ft.update(sp1_filter__in=sp1_ids, display=True)
    interest_sp1s = interestList.filter(**sp1_ft).values("sp1_filter__id").annotate(
        total=Count("sp1_filter__id"))
    interest_sp1s_mapping = dict()
    [interest_sp1s_mapping.update({interest_sp1.get("sp1_filter__id"): interest_sp1.get("total", 0)}) for interest_sp1
     in interest_sp1s]
    for sp1_id in sp1_ids:
        count_list.append(interest_sp1s_mapping.get(sp1_id, 0))

    sp2_ids = [sp.id for sp in sp2]
    sp2_ft = prepare_filter(initial_dict.copy())
    sp2_ft.update(sp2_filter__in=sp2_ids, display=True)
    interest_sp2s = interestList.filter(**sp2_ft).values("sp2_filter__id").annotate(
        total=Count("sp2_filter__id"))
    interest_sp2s_mapping = dict()
    [interest_sp2s_mapping.update({interest_sp2.get("sp2_filter__id"): interest_sp2.get("total", 0)}) for interest_sp2
     in interest_sp2s]
    for sp2_id in sp2_ids:
        count_list.append(interest_sp2s_mapping.get(sp2_id, 0))

    sp3_ids = [sp.id for sp in sp3]
    sp3_ft = prepare_filter(initial_dict.copy())
    sp3_ft.update(sp3_filter__in=sp3_ids, display=True)
    interest_sp3s = interestList.filter(**sp3_ft).values("sp3_filter__id").annotate(
        total=Count("sp3_filter__id"))
    interest_sp3s_mapping = dict()
    [interest_sp3s_mapping.update({interest_sp3.get("sp3_filter__id"): interest_sp3.get("total", 0)}) for interest_sp3
     in interest_sp3s]
    for sp3_id in sp3_ids:
        count_list.append(interest_sp3s_mapping.get(sp3_id, 0))

    facility_ids = [r.id for r in facility]
    facility_ft = prepare_filter(initial_dict.copy())
    facility_ft.update(facility_filter__in=facility_ids, display=True)
    interest_facilities = interestList.filter(**facility_ft).values("facility_filter__id").annotate(
        total=Count("facility_filter__id"))
    interest_facilities_mapping = dict()
    [interest_facilities_mapping.update({interest_facility.get("facility_filter__id"): interest_facility.get("total", 0)})
     for interest_facility in interest_facilities]
    for facility_id in facility_ids:
        count_list.append(interest_facilities_mapping.get(facility_id, 0))

    service_ids = [r.id for r in service]
    service_ft = prepare_filter(initial_dict.copy())
    service_ft.update(service_filter__in=service_ids, display=True)
    interest_services = interestList.filter(**service_ft).values("service_filter__id").annotate(total=Count("service_filter__id"))
    interest_services_mapping = dict()
    [interest_services_mapping.update({interest_service.get("service_filter__id"): interest_service.get("total", 0)}) for interest_service in interest_services]
    for service_id in service_ids:
        count_list.append(interest_services_mapping.get(service_id, 0))

    count_result = count_list + count_list

    data = render_to_string("ajax/interest_list.html", {
        "info1_label": config.LABEL_INFO1,
        "info2_label": config.LABEL_INFO2,
        "info3_label": config.LABEL_INFO3,
        "info4_label": config.LABEL_INFO4,
        "info5_label": config.LABEL_INFO5,

        "page_type": page_type,
        "interests": interests,
        "interests_id": interests_id,
        "per_page": per_page,
        "num_pages": num_pages,
        "current_page": current_page,
        "page_range": page_range,
    })
    return JsonResponse({'data': data, 'total_interests': total_interests, 'count_result': count_result})


def load_more_data(request):
    page_type = request.GET.get('pageType')
    currentInterests = request.GET.get('currentInterests')
    currentInterests = currentInterests.strip('][').split(', ')
    
    # interests_qs = cache.get('currentInterests')
    interests_qs = Interest.objects.filter(id__in=currentInterests, display=True).distinct().order_by("-rating")
    total_interests = interests_qs.count()
    interests_id = list(interests_qs.values_list('id', flat=True))

    # Pagination
    # per_page = int(cache.get('perPage'))
    per_page = int(request.GET.get('perPage'))
    num_pages = int(total_interests/per_page) + (total_interests % per_page > 0)
    current_page = int(request.GET.get('currentPage'))
    page_range = [i for i in range(1, num_pages + 1)]

    interests = interests_qs[((current_page-1)*per_page):(current_page*per_page)]

    data = render_to_string("ajax/interest_list.html", {
        "info1_label": config.LABEL_INFO1,
        "info2_label": config.LABEL_INFO2,
        "info3_label": config.LABEL_INFO3,
        "info4_label": config.LABEL_INFO4,
        "info5_label": config.LABEL_INFO5,

        "page_type": page_type,
        "interests": interests,
        "interests_id": interests_id,
        "per_page": per_page,
        "num_pages": num_pages,
        "current_page": current_page,
        "page_range": page_range,
    })
    return JsonResponse({'data': data, 'total_interests': total_interests})
