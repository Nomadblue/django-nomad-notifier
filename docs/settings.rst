========
Settings
========

SEND_EMAIL_NOTIFICATIONS
------------------------

Default: ``False``

Set this to ``True`` to enable the app to send email notifications. It is
disabled by default to avoid unwanted "surprises" (e.g. sending emails to real
users by mistake), so we force you to explicitly set it up.

NOTI_FAIL_SILENTLY
------------------

Optional setting
Default: ``False``

If there is an error sending a notification via email, the SMTP exception is
captured and stored in the object. By default, the exception is thrown and the
application fails, but if setting is present and set to ``True``, it will fail
silently and not crash. It is sometimes for production servers, where we do not
want errors to break our user experiences. 
