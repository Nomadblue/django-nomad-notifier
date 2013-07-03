=====================
Django Nomad Notifier
=====================

Overview
========

This Django app provides a way to implement a system of notifications for
the users of web apps that tipically must receive updates from the site activity
through channels such as emails (they call them "transactional emails" nowadays)
and displayed/listed on UI ("ala" social apps such as Facebook or Google+).

By itself, this plugin cannot be used. You must tipically subclass its
``Notification`` model, and mix it with ``NotificationMixin``.

Read the latest documentation on `Read the docs`_ for installation,
configuration and customization instructions.

.. _`Read the docs`: http://readthedocs.org/docs/django-nomad-notifier/en/latest/

