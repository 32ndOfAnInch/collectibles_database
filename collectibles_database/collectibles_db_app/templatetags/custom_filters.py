from django import template

register = template.Library()

@register.filter
def toggle_order(order):
    return 'desc' if order == 'asc' else 'asc'
