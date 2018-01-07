import os
import re

from setuptools import find_packages, setup


def get_long_description():
    for filename in ('README.rst',):
        with open(filename, 'r') as f:
            yield f.read()


def get_version(package):
    with open(os.path.join(package, '__init__.py')) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name='django-graphql-jwt',
    version=get_version('graphql_jwt'),
    license='MIT',
    description='JSON Web Token for GraphQL',
    long_description='\n\n'.join(get_long_description()),
    author='mongkok',
    author_email='domake.io@gmail.com',
    maintainer='mongkok',
    url='https://github.com/flavors/graphql-jwt/',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django>=1.11',
        'django-environ>=0.4.4',
        'graphene-django>=2.0.0',
        'PyJWT>=1.5.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    zip_safe=False,
    tests_require=[
        'Django>=1.11',
        'django-environ>=0.4.4',
        'coverage>=4.4',
        'graphene-django>=2.0.0',
        'PyJWT>=1.5.0',
    ],
    package_data={
        'graphql_jwt': [
            'locale/*/LC_MESSAGES/django.po',
            'locale/*/LC_MESSAGES/django.mo',
        ],
    },
)
