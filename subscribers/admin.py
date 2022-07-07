from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Subscriber


class SubscriberAdmin(ModelAdmin):
    model = Subscriber
    menu_label = "Suscribers"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "nickname", "full_name")
    search_fields = ("email", "nickname", "full_name")


modeladmin_register(SubscriberAdmin)
