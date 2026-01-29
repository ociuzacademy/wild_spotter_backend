from django import template

register = template.Library()

@register.filter
def avg(values, field_name):
    total = sum(getattr(v, field_name) for v in values)
    count = len(values)
    return total / count if count else 0
