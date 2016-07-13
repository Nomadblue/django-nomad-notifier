from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.utils import translation

from model_utils.managers import InheritanceManager


class Notification(models.Model):

    ALL_TYPE_NOTI = 1
    WEB_NOTI = 2  # Filter by WEB_NOTI to display web notifications list
    EMAIL_NOTI = 3
    NOTIFICATION_TYPE_CHOICES = (
        (ALL_TYPE_NOTI, 'Full notification'),
        (WEB_NOTI, 'Web only notification'),
        (EMAIL_NOTI, 'Email only notification'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='notifications')
    noti_type = models.PositiveSmallIntegerField(choices=NOTIFICATION_TYPE_CHOICES, default=ALL_TYPE_NOTI)
    creation_dt = models.DateTimeField(auto_now_add=True)
    displayed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    delivery_response = models.TextField(blank=True, help_text='SMTP error codes and messages')

    objects = InheritanceManager()

    web_noti_tmpl_suffix = '_web_noti_item.html'

    def save(self, *args, **kwargs):
        if getattr(self, 'notification_type', None):
            self.noti_type = self.notification_type
        return super(Notification, self).save(*args, **kwargs)

    def get_notification_obj(self):
        return Notification.objects.get_subclass(id=self.id)

    @property
    def web_noti_tmpl(self):
        template = '%s/includes/%s%s' % (self._meta.app_label, self.model_tmpl_part, self.web_noti_tmpl_suffix)
        return template

    @classmethod
    def get_auto_web_noti_tmpl(cls):
        """
        Use this method to get the tmpl you need to create in order to use
        the auto-generated tmpl path. Examples:

        >>> model = YourNotiClass
        >>> model.get_auto_web_noti_tmpl()

        """
        template = '%s/templates/%s/includes/%s%s' % (cls._meta.app_label, cls._meta.app_label, cls.model_tmpl_part, cls.web_noti_tmpl_suffix)
        return template


class NotificationMixin(object):
    """
    Adds methods to deliver email.
    """
    from_email = settings.DEFAULT_FROM_EMAIL

    email_subject_tmpl = None
    email_subject_tmpl_suffix = '_subject.txt'
    email_plaintext_body_tmpl = None
    email_plaintext_body_tmpl_suffix = '_plaintext_body.txt'
    email_html_body_tmpl = None
    email_html_body_tmpl_suffix = '_html_body.html'

    def _render_tmpl(self, template):
        ctxt = self.get_context()

        # Define SITE_URL in settings so templates can build absolute urls
        ctxt['site_url'] = getattr(settings, 'SITE_URL', None)

        # Translate templates
        if self.get_language() is not None:
            translation.activate(self.get_language())

        return render_to_string(template, ctxt)

    def get_context(self):
        """You may want to override this in your class"""
        return {}

    def get_language(self):
        """If implemented, is used in `_render_tmpl` to translate tmpl"""
        return None

    def get_attachment_files(self):
        """If implemented, the list of files this returns will be attached to the outgoing email"""
        return list()

    def get_cc_recipients_list(self):
        """If implemented, the list of receipients will be cc'ed in the notification"""
        return list()

    @classmethod
    def get_auto_email_field_tmpl(cls, attr_name):
        """
        Use this method to get the tmpl you need to create in order to use
        the auto-generated tmpl paths. Examples:

        >>> model = YourNotiClass
        >>> model.get_auto_email_field_tmpl('email_subject_tmpl')
        >>> model.get_auto_email_field_tmpl('email_plaintext_body_tmpl')
        >>> model.get_auto_email_field_tmpl('email_html_body_tmpl')

        """
        suffix = '%s_suffix' % attr_name
        template = '%s/templates/%s/emails/%s%s' % (cls._meta.app_label, cls._meta.app_label, cls.model_tmpl_part, getattr(cls, suffix, ''))
        return template

    def _get_email_field(self, attr_name, method_name):
        suffix = '%s_suffix' % attr_name
        template = '%s/emails/%s%s' % (self._meta.app_label, self.model_tmpl_part, getattr(self, suffix, ''))

        # Try auto-generation of tmpl path
        try:
            return self._render_tmpl(template)
        except TemplateDoesNotExist:
            # Try getting tmpl path from attribute defined in class using mixin
            template = getattr(self, attr_name, None)
            if template is None:
                raise ImproperlyConfigured(u"%(cls)s is missing a template."
                                           u"Define %(cls)s.model_tmpl_part, define %(cls)s.%(attr)s, or override "
                                           u"%(cls)s.%(method_name)s()." % {'attr': attr_name, "cls": self.__class__.__name__, 'method_name': method_name})
        return self._render_tmpl(template)

    def get_email_subject(self):
        """
        WARNING: It is MANDATORY to override method if you are going to
        send email using the  `send_notification_email` method.
        Your class must define an `email_subject_tmpl` attribute
        containing a template path to a file that has your email subject.
        """
        return self._get_email_field('email_subject_tmpl', 'get_email_subject')

    def get_email_plaintext_body(self):
        """
        WARNING: It is MANDATORY to override method if you are going to
        send email using the  `send_notification_email` method.
        Your class must define an `get_email_plaintext_body` attribute
        containing a template path to a file that has the plaintext version
        of your email body.
        """
        return self._get_email_field('email_plaintext_body_tmpl', 'get_email_plaintext_body')

    def get_email_html_body(self):
        """
        Your class must define an `get_email_html_body` attribute
        containing a template path to a file that has the html version
        of your email body.
        """
        try:
            return self._get_email_field('email_html_body_tmpl', 'get_email_html_body')
        except ImproperlyConfigured:
            return None

    def get_from_email(self):
        if not self.from_email:
            raise ImproperlyConfigured("You must define DEFAULT_FROM_EMAIL setting")
        return self.from_email

    def get_email_headers(self):
        """
        WARNING: It is MANDATORY to override method if you are going to
        send email using the  `send_notification_email` method.
        Must return a dict of email header keys and values that
        will be used by `EmailMultiAlternatives` class in the
        `send_notification_email` method.
        """
        raise NotImplementedError  # Must be implemented by class using mixin

    def get_recipients_list(self):
        """
        WARNING: It is MANDATORY to override method if you are going to
        send email using the  `send_notification_email` method.
        Must return a list of email recipients that
        will be used by `EmailMultiAlternatives` class in the
        `send_notification_email` method.
        """
        raise NotImplementedError  # Must be implemented by class using mixin

    def send_notification_email(self):
        if getattr(settings, 'SEND_EMAIL_NOTIFICATIONS', False):

            # From email and headers
            from_email = self.get_from_email()
            headers = self.get_email_headers()

            # Recipients
            recipients = getattr(settings, 'TEST_NOTIFICATIONS_RECIPIENTS', False)
            if recipients:
                recipients = [recipient.strip() for recipient in recipients]
            else:
                recipients = self.get_recipients_list()

            # CC recipients
            cc_recipients = self.get_cc_recipients_list()

            # Prepare subject and body
            subject = self.get_email_subject().strip()
            plaintext_body = self.get_email_plaintext_body()
            html_body = self.get_email_html_body()

            # Prepare message
            msg = EmailMultiAlternatives(subject, plaintext_body, from_email, recipients, headers=headers, cc=cc_recipients)
            if html_body:
                msg.attach_alternative(html_body, 'text/html')

            # Add attachments
            attachment_files = self.get_attachment_files()
            for att in attachment_files:
                msg.attach(att.name, att.read())

            try:
                msg.send()
            except Exception as exc:
                # Store error msg
                smtp_code = getattr(exc, 'smtp_code', '')
                smtp_error = getattr(exc, 'smtp_error', '')
                error_msg = getattr(exc, 'message', '')
                self.delivery_response = "Exception: %s\nSMTP code: %s\nSMTP error: %s\nMessage: %s" % (repr(exc), smtp_code, smtp_error, error_msg)
                self.save()
                # Not failing silently is default behaviour
                if not getattr(settings, 'NOTI_FAIL_SILENTLY', False):
                    raise
            else:
                self.email_sent = True
                self.save()
