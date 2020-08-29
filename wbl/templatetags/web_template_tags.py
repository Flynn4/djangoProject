import re
import datetime
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from wbl.models import Task

register = template.Library()


@register.simple_tag
def findTasks(user, tasks):
    return tasks.filter(students__exact=user)
