# search.templatetags.class_name.py
from django import template

register = template.Library()

@register.filter()
def tag_to_val(value):
    if value =='O':
        return "<span class='badge badge-warning'>Ordered</span>"
    elif value == 'CO':
        return "<span class='badge badge-info'>Confirmed</span>"
    elif value == 'S':
        return "<span class='badge badge-success'>Fulfilled</span>"
    else:
        return "<span class='badge badge-danger'>Cancelled</span>"


