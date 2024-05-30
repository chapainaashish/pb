from django import forms
# ======================================================================================
# MAIN
INTEREST = "Restaurant"
DOMAIN = "https://world.top25restaurants.com"
FAVICON = "img/t25r-favicon.png"
DEFAULT_TO_EMAIL = "editor@top25restaurants.com"

# ======================================================================================
# accounts/views.py
SUBMIT_INTEREST_SLUG = "nominate-a-restaurant"

# ======================================================================================
# Path on urls.py
EDIT_INTEREST_PATH = "edit-a-restaurant/<str:interest>/"
INTEREST_REVIEW_PATH = "review/<str:parent>/<str:region>/restaurant/<slug:slug>/"
INTEREST_WITHOUT_PARENT_REVIEW_PATH = "review/<str:region>/restaurant/<slug:slug>/"
INTEREST_DETAIL_PATH = "<str:parent>/<str:region>/restaurant/<slug:slug>/"
INTEREST_DETAIL_WITHOUT_PARENT_PATH = "<str:region>/restaurant/<slug:slug>/"

# ======================================================================================
# filters/models.py
# label on admin:
VERBOSE_NAME_WORLD = "World"
VERBOSE_NAME_COUNTRY = "Destination"
VERBOSE_NAME_REGION = "Region"
VERBOSE_NAME_CITY = "City"
VERBOSE_NAME_FACILITY = "Inside"
VERBOSE_NAME_SERVICE = "Services"
VERBOSE_NAME_RATING = "Awards"
VERBOSE_NAME_SP1 = "Cuisine"
VERBOSE_NAME_SP2 = "Style"
VERBOSE_NAME_SP3 = "Pricing"

VERBOSE_NAME_PLURAL_WORLD = "World"
VERBOSE_NAME_PLURAL_COUNTRY = "Destinations"
VERBOSE_NAME_PLURAL_REGION = "Regions"
VERBOSE_NAME_PLURAL_CITY = "Cities"
VERBOSE_NAME_PLURAL_FACILITY = "Inside"
VERBOSE_NAME_PLURAL_SERVICE = "Service"
VERBOSE_NAME_PLURAL_RATING = "Award"
VERBOSE_NAME_PLURAL_SP1 = "Cuisine"
VERBOSE_NAME_PLURAL_SP2 = "Style"
VERBOSE_NAME_PLURAL_SP3 = "Pricing"

# pages_app/context_processors.py
# label on frontend:
WORLD_TEXT = "Region"
COUNTRY_TEXT = "Destination"
REGION_TEXT = "Region"
CITY_TEXT = "City"
FACILITY_TEXT = "Inside"
SERVICE_TEXT = "Services"
RATING_TEXT = "Awards"
SP1_TEXT = "Cuisine"
SP2_TEXT = "Style"
SP3_TEXT = "Pricing"

# icon on frontend:
WORLD_ICON = "bi bi-globe2"
COUNTRY_ICON = "bi bi-geo-alt"
REGION_ICON = "bi bi-geo-fill"
CITY_ICON = "bi bi-buildings"
FACILITY_ICON = "bi bi-flower2"
SERVICE_ICON = "bi bi-people"
RATING_ICON = "bi bi-trophy"
SP1_ICON = "bi bi-droplet"
SP2_ICON = "bi bi-droplet"
SP3_ICON = "bi bi-coin"

# activate filters
ACTIVATE_WORLD = False
ACTIVATE_COUNTRY = True
ACTIVATE_REGION = False
ACTIVATE_CITY = True
ACTIVATE_FACILITY = True
ACTIVATE_SERVICE = True
ACTIVATE_RATING = True
ACTIVATE_SP1 = True
ACTIVATE_SP2 = False
ACTIVATE_SP3 = True

# ======================================================================================
# interests/forms.py
INTEREST_FORM_FIELDS = [
    "name", "text", "info1", "info2", "info4", "info5", "long_info1", 
    "region", "regions", "cover", "email2", "address", "website", 
    "web_text", "website2", "web_text2", "number"
]

INTEREST_FORM_LABELS = {
    "name": "Restaurant Name*",
    "text": "Restaurant description and information*",
    "info1": "Location*",
    "info2": "Cuisine*",
    "info4": "Seating capacity*",
    "info5": "Name of your Chef*",
    "long_info1": "Opening hours*",
    "region": "Geographic location (select)*",
    "regions": "Country or Region (select)*",
    "cover": "Upload Main Photo (min. width 900px)*",
    "email2": "Email*",
    "address": "Address*",
    "website": "Website address*",
    "web_text": "Website title*",
    "website2": "Reservation link",
    "web_text2": "Reservation link title",
    "number": "Phone number*",
}

INTEREST_FORM_WIDGETS = {
    "name": forms.TextInput(attrs={"placeholder": "Name of your restaurant...", "class": "w-75 bg-light", "required": True}),
    "info1": forms.TextInput(attrs={"placeholder": "Where is your restaurant located: landmark, region and country...", "class": "w-75 bg-light", "required": True}),
    "info2": forms.TextInput(attrs={"placeholder": "What describes best your cuisine style...", "class": "w-75 bg-light", "required": True}),
    "info4": forms.TextInput(attrs={"placeholder": "Capacity of your restaurant, including private rooms, bars...", "class": "w-75 bg-light", "required": True}),
    "info5": forms.TextInput(attrs={"placeholder": "Name of your Chef, Chef de Cuisine, Owner, or...", "class": "w-75 bg-light", "required": True}),
    "long_info1": forms.TextInput(attrs={"placeholder": "Opening hours and reservation conditions...", "class": "w-75 bg-light", "required": True}),
    "email2": forms.EmailInput(attrs={"placeholder": "Main email address, if multiple separate with comma...", "class": "w-75 bg-light", "required": True}),
    "address": forms.Textarea(attrs={"placeholder": "Physical location with building, street, city, zip code, country...", "class": "w-75 bg-light", "required": True}),
    "web_text": forms.TextInput(attrs={"placeholder": "Website title or name", "class": "w-75 bg-light", "required": True}),
    "website": forms.TextInput(attrs={"placeholder": "Website full url for link...", "class": "w-75 bg-light", "required": True}),
    "web_text2": forms.TextInput(attrs={"placeholder": "Reservation title or name", "class": "w-75 bg-light", "required": False}),
    "website2": forms.TextInput(attrs={"placeholder": "Reservation link", "class": "w-75 bg-light", "required": False}),
    "number": forms.TextInput(attrs={"placeholder": "Phone Number, main number to book a table...", "class": "w-75 bg-light", "required": True}),
}

PLACEHOLDER_TEXT = "Add here a description and all information about restaurant: History, Estate, Terroir, Cuisinemaker and team, Cuisines, etc..."

# ======================================================================================
# interests/models.py
LABEL_INFO1 = "Location"
LABEL_INFO2 = "Cuisine"
LABEL_INFO3 = "Pricing"
LABEL_INFO4 = "Seating"
LABEL_INFO5 = "Chef"
LABEL_LONG_INFO1 = "Opening Hours"
LABEL_WEB2_INFO = "Book a Table"
LABEL_WEB2_INFO_ADMIN = "Reservation"

# ======================================================================================
# interests/views.py
LABEL_RR_FORM1 = "Would you recommend this restaurant to a friend?"
LABEL_RR_FORM2 = "Restaurant location:"
LABEL_RR_FORM3 = "Ambience & Comfort:"
LABEL_RR_FORM4 = "Food, Cooking & Presentation:"
LABEL_RR_FORM5 = "Chef's Personality & Service:"
LABEL_RR_FORM6 = "Value for money:"
