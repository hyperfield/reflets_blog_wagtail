from hitcount.models import HitCount
from hitcount.views import HitCountMixin

from wagtail.core import hooks

from .models import BlogPage


@hooks.register("before_serve_page")
def increment_view_count(page, request, serve_args, serve_kwargs):
    if page.specific_class == BlogPage:
        hit_count = HitCount.objects.get_for_object(page)
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
