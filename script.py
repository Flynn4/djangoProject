import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'djangoProject.settings')

import django

django.setup()
from wbl.models import *


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

    users = [
        {'username': 'mentor1', 'password': 123456, 'email': 'mentor1@mentor1.com'},
        {'username': 'mentor2', 'password': 123456, 'email': 'mentor2@mentor2.com'},
        {'username': 'mentor3', 'password': 123456, 'email': 'mentor3@mentor3.com'},
        {'username': 'mentor4', 'password': 123456, 'email': 'mentor4@mentor4.com'},
        {'username': 'mentor5', 'password': 123456, 'email': 'mentor5@mentor5.com'},
        {'username': 'mentor6', 'password': 123456, 'email': 'mentor6@mentor6.com'},
        {'username': 'mentor7', 'password': 123456, 'email': 'mentor7@mentor7.com'},
        {'username': 'mentor8', 'password': 123456, 'email': 'mentor8@mentor8.com'},
        {'username': 'mentor9', 'password': 123456, 'email': 'mentor9@mentor9.com'},
        {'username': 'mentor10', 'password': 123456, 'email': 'mentor10@mentor10.com'},
    ]

    for r in roles:
        add_roles(r['name'])

    criterions = [
        {'name': 'Project management',  # id:1
         'detail': 'Test Detail for Project management'},
        {'name': 'Requirement analysis',  # id:2
         'detail': 'Test Detail for Requirement analysis'},
        {'name': "Software design",  # id:3
         'detail': 'Test Detail for Software design'},
        {'name': 'Programming Quality/Tests',  # id:4
         'detail': 'Test Detail for Programming Quality/Tests'},
        {'name': 'Adaptation and use of tools to support influenced areas',  # id:5
         'detail': 'Test Detail for Adaptation and use of tools to support influenced areas'},
        {'name': 'Communication',  # id:6
         'detail': 'Test Detail for Communication'},
        {'name': 'Motivation',  # id:7
         'detail': 'Test Detail for Motivation'},
        {'name': 'Desires to contribute',  # id:8
         'detail': 'Test Detail for Desires to contribute'},
        {'name': 'Capability to learn alone, take risks, etc.',  # id:9
         'detail': 'Test Detail for Capability to learn alone, take risks, etc.'},
        {'name': 'Balance the necessary resources to satisfy multiple goals',  # id:10
         'detail': 'Test Detail for Balance the necessary resources to satisfy multiple goals'},
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

    for u in users:
        add_user(u['username'], u['password'], u['email'])


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


def add_user(username, password, email):
    u = User.objects.get_or_create(username=username, password=password, email=email)[0]
    u.save()
    return u


# Start execution here!
if __name__ == '__main__':
    print('Starting population script...')
    populate()
