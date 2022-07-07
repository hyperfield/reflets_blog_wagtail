from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import BlogUser


class BlogUserAdmin(ModelAdmin):
    model = BlogUser
    menu_label = "Blog users"
    menu_icon = "placeholder"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "nickname", "full_name")
    search_fields = ("email", "nickname", "full_name")


modeladmin_register(BlogUserAdmin)
