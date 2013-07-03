import os
from distutils.core import setup

package_dirs = ('nomadlytics',)

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
            if dirname.startswith('.'): del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

doc_dir = os.path.join(os.path.dirname(__file__), 'docs')
version_num = __import__('nomadlytics').__version__

setup(
    name='django-nomadlytics',
    version=version_num,
    description='Django app to track stats to any analytics SaaS using libsaas and celery.',
    long_description=open('README.rst').read(),
    author='Hector Garcia',
    author_email='hector@nomadblue.com',
    url='https://github.com/Nomadblue/django-nomadlytics',
    download_url="https://github.com/Nomadblue/django-nomadlytics/zipball/v%s" % version_num,
    packages=packages,
    data_files=data_files,
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

