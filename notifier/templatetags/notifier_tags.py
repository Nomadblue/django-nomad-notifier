from django import template


register = template.Library()


@register.assignment_tag
def get_new_notifications_count(user):
    """Usually used to display an unread notifications counter"""
    from notifier.models import Notification
    return user.notifications.exclude(noti_type=Notification.EMAIL_NOTI).filter(displayed=False).count()
