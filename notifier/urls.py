from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from notifier.views import NotificationsListView, ClearAllNotificationsView, ClearNotificationView, DeleteNotificationView


urlpatterns = [
    url(r'^$', login_required(NotificationsListView.as_view()), name='notifications_list'),
    url(r'^clear/all/$', login_required(ClearAllNotificationsView.as_view()), name='clear_all_notifications'),
    url(r'^(?P<pk>\d+)/clear/$', login_required(ClearNotificationView.as_view()), name='clear_notification'),
    url(r'^(?P<pk>\d+)/delete/$', login_required(DeleteNotificationView.as_view()), name='delete_notification'),
]
