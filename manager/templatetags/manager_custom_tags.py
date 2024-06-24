from django import template
import os

from django.conf import settings

register = template.Library()


@register.inclusion_tag(os.path.join(settings.COMPONENTS_DIRS.get('manager'), "topbar.html"))
def topbar(title, user, *args, **kwargs):
  
  data = {
    'title': title,
    'user': user,
  }
  
  return data

