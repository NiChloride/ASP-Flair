from django import template

register = template.Library()

@register.filter
def total_weight(order):
    return order.total_weight()