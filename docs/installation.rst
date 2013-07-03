============
Installation
============

Initial setup
=============

The package is listed in the `Python Package Index`_. You can use your favorite
package manager like ``easy_install`` or ``pip``::

    pip install django-nomad-notifier

Or, you can clone the latest development code from its repository::

    git clone git@github.com:Nomadblue/django-nomad-notifier.git

.. _Python Package Index: http://pypi.python.org/pypi/django-nomad-notifier/

Add ``notifier`` to the ``INSTALLED_APPS`` setting of your ``settings.py``::

    INSTALLED_APPS = (
        ...
        'notifier',
    )

