from django import template

register = template.Library()

@register.filter
def getCombinedWeight(order):
    return order.getCombinedWeight()