import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'djangoProject.settings')

import django
import requests
import json

django.setup()
from wbl.models import *
import re


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    roles = [
        {'name': 'Project manager'},  # id:1
        {'name': 'Analyst'},  # id:2
        {'name': 'Software designer'},  # id:3
        {'name': 'Programmer'},  # id:4
        {'name': 'Validation and verification engineer'},  # id:5
        {'name': 'Configuration manager'},  # id:6
        {'name': 'Quality engineer'},  # id:7
        {'name': 'Test engineer'},  # id:8
        {'name': 'Documentator'},  # id:9
        {'name': 'Maintenance engineer'},  # id:10
    ]

    for r in roles:
        add_roles(r['name'])

    criterions = [
        {'name': 'Project management',  # id:1
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Requirement analysis',  # id:2
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': "Software design",  # id:3
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Programming Quality/Tests',  # id:4
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Adaptation and use of tools to support influenced areas',  # id:5
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Communication',  # id:6
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Motivation',  # id:7
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Desires to contribute',  # id:8
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Capability to learn alone, take risks, etc.',  # id:9
         'detail': 'testttttttttttttttttttttttttt'},
        {'name': 'Balance the necessary resources to satisfy multiple goals',  # id:10
         'detail': 'testttttttttttttttttttttttttt'},
    ]

    for c in criterions:
        add_criterions(c['name'], c['detail'])

    role_have_criterion(1, 5)
    role_have_criterion(1, 6)
    role_have_criterion(1, 7)
    role_have_criterion(1, 8)
    role_have_criterion(1, 9)

    role_have_criterion(2, 1)
    role_have_criterion(2, 2)
    role_have_criterion(2, 4)
    role_have_criterion(2, 7)
    role_have_criterion(2, 8)

    role_have_criterion(3, 1)
    role_have_criterion(3, 4)
    role_have_criterion(3, 5)
    role_have_criterion(3, 9)
    role_have_criterion(3, 10)

    role_have_criterion(4, 1)
    role_have_criterion(4, 5)
    role_have_criterion(4, 6)
    role_have_criterion(4, 8)
    role_have_criterion(4, 10)

    role_have_criterion(5, 5)
    role_have_criterion(5, 7)
    role_have_criterion(5, 8)
    role_have_criterion(5, 9)
    role_have_criterion(5, 10)

    for rc in range(6, 11):
        role_have_criterion(rc, 1)
        role_have_criterion(rc, 2)
        role_have_criterion(rc, 3)
        role_have_criterion(rc, 4)
        role_have_criterion(rc, 5)


def add_roles(name):
    r = Role.objects.get_or_create(name=name)[0]
    r.save()
    return r


def add_criterions(name, detail):
    c = Criterion.objects.get_or_create(name=name, detail=detail)[0]
    c.save()
    return c


def role_have_criterion(roleId, criterionId):
    r = Role.objects.get(roleId=roleId)
    c = Criterion.objects.get(criterionId=criterionId)
    r.role_have.add(c)
    r.save()
    return r


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
