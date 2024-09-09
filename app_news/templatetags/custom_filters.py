from django import template

register = template.Library()

@register.filter(name='cut_until_dot')
def cut_until_dot(value):
    if isinstance(value, str):
        return value.partition('.')[0]
    return value