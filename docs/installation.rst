============
Installation
============

Dependencies
============

* django-model-utils: https://github.com/carljm/django-model-utils/

Initial setup
=============

The package is listed in the `Python Package Index`_. You can use your favorite
package manager like ``easy_install`` or ``pip``::

    pip install django-nomad-notifier

Or, you can clone the latest development code from its repository and add the
folder to your python path. For example, if you use `virtualenvwrapper`_::

    git clone git@github.com:Nomadblue/django-nomad-notifier.git
    add2virtualenv django-nomad-notifier/

.. _`Python Package Index`: http://pypi.python.org/pypi/django-nomad-notifier/
.. _`virtualenvwrapper`: http://virtualenvwrapper.readthedocs.org/en/latest/

Add ``notifier`` to the ``INSTALLED_APPS`` setting of your ``settings.py``::

    INSTALLED_APPS = (
        ...
        'notifier',
    )

We use migrations to nicely update our database with the
``Notification`` model schema. But **wait**! Since there are models that
depend on custom user (``settings.AUTH_USER_MODEL``), we cannot provide the
migrations with the package. Instead, our policy at Nomadblue is to create
them out of the scope in another place.

Prior to Django 1.7, there was `South`_ . So, for example, in an app called
``website`` it would be::

    SOUTH_MIGRATION_MODULES = {
        'notifier': 'website.notifier_migrations',
    }

From your project root, create the initial migration and apply it::

    python manage.py schemamigration notifier --initial
    python manage.py migrate notifier

.. _`South`: http://south.aeracode.org/

In Django 1.7 or beyond, where South was incorporated as part of the core,
the equivalent setting is::

    MIGRATION_MODULES = {
        'notifier': 'website.notifier_migrations',
    }

From your project root, create the initial migration and apply it::

    python manage.py makemigrations notifier
    python manage.py migrate notifier

If you prefer not to use migrations, can sync with the Django command::

    python manage.py syncdb

Finally, if you want to enable email notifications (disabled by default),
you **must** set the following in your ``settings.py``::

    SEND_EMAIL_NOTIFICATIONS = True
