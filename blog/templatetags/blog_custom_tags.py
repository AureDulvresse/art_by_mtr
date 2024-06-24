from django import template
import os

from django.conf import settings

register = template.Library()

@register.inclusion_tag(os.path.join(settings.COMPONENTS_DIRS.get('global'), "breadcrumb.html"))
def breadcrumb(title, msg, user, cart_items, *args, **kwargs):
  
  data = {
    'title': title,
    'msg': msg,
    'user': user,
    'preview_cart_items': cart_items,
  }
  
  return data

@register.inclusion_tag(os.path.join(settings.COMPONENTS_DIRS.get('blog'), "post-card.html"))
def postCard(post, *args, **kwargs):
  
  data = {
    'post': post,
  }
  
  return data