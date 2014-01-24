from django import template


register = template.Library()


@register.assignment_tag
def get_new_notifications_count(user):
    """Usually used to display an unread notifications counter"""
    return user.notifications.filter(displayed=False).count()
