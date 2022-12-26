from datetime import date, datetime
from django.utils.timezone import is_aware, utc

from django import template
register = template.Library()

@register.filter
def time_since(value, default="just"):
    if not isinstance(value, date):  # datetime is a subclass of date
        return value
    now = datetime.now(utc if is_aware(value) else None)
    diff = now - value
    periods = (
        (diff.days / 365, " year"),
        (diff.days / 30, " months"),
        (diff.days / 7, " weeks"),
        (diff.days, " days"),
        (diff.seconds / 3600, " hours"),
        (diff.seconds / 60, " minutes"),
        (diff.seconds, " seconds"),
    )
    for period, singular in periods:
        if int(period) > 0:
            return "%d%s ago" % (period, singular)
    return default

@register.simple_tag
def user_liked_class(video, user):
    liked = video.user_liked(user)
    if liked == 0:
        return "red"
    else:
        return "grey"

@register.simple_tag
def user_collected_class(video, user):
    collected = video.user_collected(user)
    if collected == 0:
        return "red"
    else:
        return "grey"