#!/usr/bin/env python

import io
import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup


def get_long_description():
    for filename in ('README.rst',):
        with io.open(filename, 'r', encoding='utf-8') as f:
            yield f.read()


def get_version(package):
    with io.open(os.path.join(package, '__init__.py')) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


setup(
    name='django-graphql-jwt',
    version=get_version('graphql_jwt'),
    license='MIT',
    description='JSON Web Token for Django GraphQL',
    long_description='\n\n'.join(get_long_description()),
    author='mongkok',
    author_email='domake.io@gmail.com',
    maintainer='mongkok',
    url='https://github.com/flavors/django-graphql-jwt',
    project_urls=OrderedDict((
        ('Documentation', 'https://django-graphql-jwt.domake.io'),
        ('Issues', 'https://github.com/flavors/django-graphql-jwt/issues'),
    )),
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Django>=1.11',
        'graphene-django>=3.0.0b1',
        'PyJWT>=2,<3',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
    ],
    zip_safe=False,
    package_data={
        'graphql_jwt': [
            'locale/*/LC_MESSAGES/django.po',
            'locale/*/LC_MESSAGES/django.mo',
            'refresh_token/locale/*/LC_MESSAGES/django.po',
            'refresh_token/locale/*/LC_MESSAGES/django.mo',
        ],
    },
)
