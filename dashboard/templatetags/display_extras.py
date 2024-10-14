import humanize
from django import template

register = template.Library()


def naturaldelta(s) -> str:
    out = humanize.naturaldelta(s)
    if out == "a day":
        return "day"
    else:
        return out


register.filter("naturaldelta", naturaldelta)
