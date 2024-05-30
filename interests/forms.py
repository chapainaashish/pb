from base import config
from django import forms
from .models import ReviewAndRating, Interest, Comment
from filters.models import World, Country, Region, City, Facility, Service, Rating, SP1, SP2, SP3
from captcha.fields import CaptchaField
from django.core.files.images import get_image_dimensions


class ReviewRatingForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = ReviewAndRating
        fields = [
            'recommended', 'value', 'service', 'cleanliness', 'location',
            'sustainability', 'title', 'review'
        ]


class InterestForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(InterestForm, self).__init__(*args, **kw)
        
        self.fields['cover'].widget.attrs['class'] = "w-75"

        self.fields['region'].widget.attrs['class'] = "w-75"
        self.fields['region'].widget.attrs['required'] = True

        self.fields['regions'].widget.attrs['class'] = "w-75"

        self.fields['website'].initial = "https://"
        self.fields['website2'].initial = "https://"

    captcha = CaptchaField()
    class Meta:
        model = Interest
        fields = config.INTEREST_FORM_FIELDS
        labels = config.INTEREST_FORM_LABELS
        widgets = config.INTEREST_FORM_WIDGETS

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        if not cover:
            raise forms.ValidationError("No image!")
        else:
            w, h = get_image_dimensions(cover)
            if w < 900:
                raise forms.ValidationError("The image is %i pixel wide. Minimum image width is 900px" % w)
            # if h < 900:
            #     raise forms.ValidationError("The image is %i pixel high. Minimum image height is 900px" % h)
        return cover
    

class InterestAdminForm(forms.ModelForm):
    # Define your extra field here
    add_filters = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 92, 'rows': 3}),
        required=False,
        label='Add Filters'
    )

    def save(self, commit=True):
        interest = super().save(commit=commit)
        filters_csv = self.cleaned_data.get('add_filters')
        if filters_csv:
            filters = filters_csv.split(',')
            print(filters_csv)
            for filter_name in filters:
                filter_name = filter_name.strip()
                if filter_name:
                    try:
                        facility_filter = Facility.objects.get(name=filter_name)
                        interest.facility_filter.add(facility_filter)
                    except Facility.DoesNotExist:
                        pass

                    try:
                        service_filter = Service.objects.get(name=filter_name)
                        interest.service_filter.add(service_filter)
                    except Service.DoesNotExist:
                        pass

                    try:
                        rating_filter = Rating.objects.get(name=filter_name)
                        interest.rating_filter.add(rating_filter)
                    except Rating.DoesNotExist:
                        pass

                    try:
                        sp1_filter = SP1.objects.get(name=filter_name)
                        interest.sp1_filter.add(sp1_filter)
                    except SP1.DoesNotExist:
                        pass

                    try:
                        sp2_filter = SP2.objects.get(name=filter_name)
                        interest.sp2_filter.add(sp2_filter)
                    except SP2.DoesNotExist:
                        pass

                    try:
                        sp3_filter = SP3.objects.get(name=filter_name)
                        interest.sp3_filter.add(sp3_filter)
                    except SP3.DoesNotExist:
                        pass

        return interest

    class Meta:
        model = Interest
        fields = ['name', 'text', 'rating', 'custom_overlay', 'google_map', 
              'info1_url', 'info1', 'info2_url', 'info2', 'info3_url', 'info3', 
              'info4_url', 'info4', 'info5_url', 'info5', 'long_info1', 
              'region', 'regions', 'cover', 'cover2', 'sidebar', 'ad_manager', 
              'meta_description', 'meta_keywords', 'logo_on_navbar', 
              'list_carousel', 'carousel_title', 'top_slider', 'cover_slider', 
              'hide_rating', 'display', 'send_email', 'display_list', 
              'display_billboard', 'linkup_tags', 'user', 'username', 'email1', 
              'email2', 'address', 'website', 'web_text', 'website2', 
              'web_text2', 'number', 'isvalidated', 'slug', 'add_filters', 'notes']
        widgets = {
            'google_map': forms.Textarea(attrs={'cols': 92, 'rows': 6}),
            'long_info1': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'sidebar': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'ad_manager': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'meta_description': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'meta_keywords': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'linkup_tags': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'address': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
            'notes': forms.Textarea(attrs={'cols': 92, 'rows': 3}),
        }


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Comment
        fields = [
            'title', 'body'
        ]


class EmailInterestForm(forms.Form):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    email = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'type': 'email'})
    )
    subject = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
    message = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder': 'Message', 'rows': 5})
    )
    captcha = CaptchaField()
