from django import template


register = template.Library()


@register.simple_tag
def findTasks(user, tasks):
    return tasks.filter(students__exact=user)
