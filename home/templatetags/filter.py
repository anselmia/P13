from django import template

register = template.Library()


@register.filter
def round_to_int(value):
    """
    Round value to nearest int
    Returns 0 on any error.
    """
    if value is not None:
        try:
            value = int(round(value))
            return value
        except:
            pass
    return 0
