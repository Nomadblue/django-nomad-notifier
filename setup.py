import os
from distutils.core import setup

package_dirs = ('notifier',)


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
for package_dir in package_dirs:
    for dirpath, dirnames, filenames in os.walk(package_dir):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'):
                del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
        elif filenames:
            # not currently used
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

version_num = __import__('notifier').__version__

setup(
    name='django-nomad-notifier',
    version=version_num,
    description='Django app to implement a system of notifications for the users of web apps that tipically must receive updates from the site activity.',
    long_description=open('README.rst').read(),
    author='Hector Garcia',
    author_email='hector@nomadblue.com',
    url='https://github.com/Nomadblue/django-nomad-notifier',
    download_url="https://github.com/Nomadblue/django-nomad-notifier/archive/v%s.zip" % version_num,
    packages=packages,
    package_data={'notifier': ['templates/notifier/*']},  # Include templates and statics here
    install_requires=['django-model-utils'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
