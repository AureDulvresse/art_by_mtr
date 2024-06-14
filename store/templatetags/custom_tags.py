from django import template
import os

from art_by_mtr.settings import COMPONENTS_DIRS

register = template.Library()

@register.inclusion_tag(os.path.join(COMPONENTS_DIRS[0], "breadcrumb.html"))
def breadcrumb(title, msg, *args, **kwargs):
  
  data = {
    'title': title,
    'msg': msg,
  }
  
  return data

@register.inclusion_tag(os.path.join(COMPONENTS_DIRS[0], "artwork-card.html"))
def artworkCard(artwork, *args, **kwargs):
  
  data = {
    'artwork': artwork,
  }
  
  return data

@register.inclusion_tag(os.path.join(COMPONENTS_DIRS[0], "post-card.html"))
def postCard(post, *args, **kwargs):
  
  data = {
    'post': post,
  }
  
  return data