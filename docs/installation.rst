============
Installation
============

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

This app uses `South`_ migrations to nicely update your database with the
``Notification`` model schema::

    python manage.py migrate notifier

Otherwise you can go on yourself and sync with Django command::

    python manage.py syncdb

