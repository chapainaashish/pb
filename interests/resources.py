from import_export import resources, fields, widgets
from .models import Interest
from django.contrib.auth import get_user_model


User = get_user_model()


class InterestResource(resources.ModelResource):

    email2 = fields.Field(attribute="email2", column_name="email2", widget=widgets.CharWidget(), default="")
    text = fields.Field(attribute="text", column_name="text", widget=widgets.CharWidget(), default="")
    address = fields.Field(attribute="address", column_name="address", widget=widgets.CharWidget(), default="")
    website = fields.Field(attribute="website", column_name="website", widget=widgets.CharWidget(), default="")
    web_text = fields.Field(attribute="web_text", column_name="web_text", widget=widgets.CharWidget(), default="")
    website2 = fields.Field(attribute="website2", column_name="website2", widget=widgets.CharWidget(), default="")
    web_text2 = fields.Field(attribute="web_text2", column_name="web_text2", widget=widgets.CharWidget(), default="")
    number = fields.Field(attribute="number", column_name="number", widget=widgets.CharWidget(), default="")
    info1 = fields.Field(attribute="info1", column_name="info1", widget=widgets.CharWidget(), default="")
    info2 = fields.Field(attribute="info2", column_name="info2", widget=widgets.CharWidget(), default="")
    info3 = fields.Field(attribute="info3", column_name="info3", widget=widgets.CharWidget(), default="")
    info4 = fields.Field(attribute="info4", column_name="info4", widget=widgets.CharWidget(), default="")
    info5 = fields.Field(attribute="info5", column_name="info5", widget=widgets.CharWidget(), default="")
    long_info1 = fields.Field(attribute="long_info1", column_name="long_info1", widget=widgets.CharWidget(), default="")
    google_map = fields.Field(attribute="google_map", column_name="google_map", widget=widgets.CharWidget(), default="")
    info1_url = fields.Field(attribute="info1_url", column_name="info1_url", widget=widgets.CharWidget(), default="")
    info2_url = fields.Field(attribute="info2_url", column_name="info2_url", widget=widgets.CharWidget(), default="")
    info3_url = fields.Field(attribute="info3_url", column_name="info3_url", widget=widgets.CharWidget(), default="")
    info5_url = fields.Field(attribute="info5_url", column_name="info5_url", widget=widgets.CharWidget(), default="")
    linkup_tags = fields.Field(attribute="linkup_tags", column_name="linkup_tags", widget=widgets.CharWidget(), default="")
    isvalidated = fields.Field(attribute="isvalidated", column_name="isvalidated", widget=widgets.CharWidget(), default="")
    notes = fields.Field(attribute="notes", column_name="notes", widget=widgets.CharWidget(), default="")

    class Meta:
        model = Interest
        fields = ('id', 'name', 'rating', 'username', 'email2', 'text', 
        'address', 'website', 'web_text', 'website2', 'web_text2', 'number', 
        'info1', 'region', 'regions', 'info2', 'info3', 'info4', 'info5', 
        'long_info1', 'google_map', 'cover', 'info1_url', 'info2_url', 
        'info3_url', 'info5_url', 'hide_rating', 'display', 'send_email', 
        'linkup_tags', 'isvalidated', 'notes')
        export_order = ('id', 'name', 'rating', 'username', 'email2', 'text', 
        'address', 'website', 'web_text', 'website2', 'web_text2', 'number', 
        'info1', 'region', 'regions', 'info2', 'info3', 'info4', 'info5', 
        'long_info1', 'google_map', 'cover', 'info1_url', 'info2_url', 
        'info3_url', 'info5_url', 'hide_rating', 'display', 'send_email', 
        'linkup_tags', 'isvalidated', 'notes')
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True

    def after_import_instance(self, instance, new, **kwargs):
        instance.user = kwargs['user']

    def before_save_instance(self, instance, using_transactions, dry_run):
        if instance.name == "" or instance.text == "" or not instance.cover:
            instance.display = 0

        if instance.username:
            current_user = User.objects.get(username=instance.username)
            instance.user = current_user
            instance.email1 = current_user.email
        else:
            instance.username = instance.user.username
            instance.email1 = instance.user.email
        return instance
