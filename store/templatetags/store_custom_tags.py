from django import template
from django.forms.boundfield import BoundField
import os

from django.conf import settings

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if isinstance(field, BoundField):
        return field.as_widget(attrs={"class": css_class})
    return field

@register.filter(name='add_class_if_error')
def add_class_if_error(field, css_class):
    if isinstance(field, BoundField):
        if field.errors:
            css_class += ' is-invalid'
        return field.as_widget(attrs={"class": css_class})
    return field


@register.inclusion_tag(os.path.join(settings.COMPONENTS_DIRS.get('global'), "breadcrumb.html"))
def breadcrumb(title, msg, user, cart_items, *args, **kwargs):
  
  data = {
    'title': title,
    'msg': msg,
    'user': user,
    'preview_cart_items': cart_items,
  }
  
  return data

@register.inclusion_tag(os.path.join(settings.COMPONENTS_DIRS.get('store'), "artwork-card.html"))
def artworkCard(artwork, user, *args, **kwargs):
  
  data = {
    'artwork': artwork,
    'user': user,
  }
  
  return data

