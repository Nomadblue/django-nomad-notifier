# -*- coding: utf-8 -*-

from django.views.generic import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from notifier.models import Notification


class NotificationsListView(ListView):
    """Shows the list of user notifications in reverse chronological order"""
    template_name = 'notifier/notifications_list.html'
    model = Notification

    def get_queryset(self):
        return self.request.user.notifications.exclude(noti_type=Notification.EMAIL_NOTI).order_by('-creation_dt')


class ClearAllNotificationsView(View):
    """Marks all user notifications as read"""

    def dispatch(self, request, *args, **kwargs):
        request.user.notifications.filter(displayed=False).update(displayed=True)
        return redirect(reverse_lazy('notifications_list'))


class ClearNotificationView(View, SingleObjectMixin):
    """Marks notification as read"""
    model = Notification
    url = reverse_lazy('notifications_list')

    def get_object(self):
        """Only owner can update notification"""
        obj = super(ClearNotificationView, self).get_object()
        if self.request.user != obj.user:
            raise PermissionDenied
        return obj

    def dispatch(self, request, *args, **kwargs):
        """Updates notification and redirects to proper next page"""
        noti = self.get_object()
        noti.displayed = True
        noti.save()
        try:
            # Try to redirect to obj url
            self.url = noti.get_notification_obj().get_obj_url()
        except AttributeError:
            pass
        return redirect(self.url)


class DeleteNotificationView(DeleteView):
    model = Notification
    success_url = reverse_lazy('notifications_list')

    # def get_success_url(self):
    #     return self.request.user.sec_user.get_absolute_url()

    # def delete(self, request, *args, **kwargs):
    #     # SuccessMessageMixin does not apply in DeleteView:
    #     # https://code.djangoproject.com/ticket/21936
    #     messages.success(self.request, self.success_message)
    #     return super(WorkExperienceDelete, self).delete(request, *args, **kwargs)
