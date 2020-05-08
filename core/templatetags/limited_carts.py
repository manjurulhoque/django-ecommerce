from django import template
from core.models import Cart

register = template.Library()


@register.simple_tag(name='limited_carts', takes_context=True)
def limited_carts(context, n=1):
    request = context['request']
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)[:n]
    return None
