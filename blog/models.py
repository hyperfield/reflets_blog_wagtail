from django import forms
from django.db import models
from django.contrib.auth.models import User
# from users.models import BlogUser
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        blogpages = BlogPage.objects.live().public().\
            order_by('-first_published_at')
        most_viewed_pages = BlogPage.objects.live().public().\
            order_by('hit_count_generic')
        context['blogpages'] = blogpages
        # Look up at sieve blog optimization
        context['most_viewed_pages'] = most_viewed_pages[:5]
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page, HitCountMixin):
    date = models.DateField("Post date")
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               verbose_name="Author", null=True)
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    allow_comments = models.BooleanField('allow comments', default=True)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def get_absolute_url(self):
        return self.get_url()

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.FilterField('date'),
        index.FilterField('tags'),
    ]

    content_panels = Page.content_panels + [
      MultiFieldPanel([
        FieldPanel('date'),
        FieldPanel('author'),
        FieldPanel('tags'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
      ], heading="Blog information"),
      FieldPanel('intro'),
      FieldPanel('body'),
      InlinePanel('gallery_images', label="Gallery images"),
    ]

    def get_context(self, request, *args, **kwargs):
        most_viewed_pages = BlogPage.objects.live().public().\
            order_by('hit_count_generic')
        context = super().get_context(request, *args, **kwargs)
        context['most_viewed_pages'] = most_viewed_pages[:5]
        return context


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class BlogTagIndexPage(Page):
    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Blog categories'
