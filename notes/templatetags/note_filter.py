from django import template

register = template.Library()

@register.filter()
def is_even(notebook):
  return notebook.id % 2 == 0