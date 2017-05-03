from django import template
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.simple_tag
def edit(object):
    content_type = ContentType.objects.get_for_model(object.__class__)
    return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(object.id,))
