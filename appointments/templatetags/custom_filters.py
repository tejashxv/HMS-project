from django import template

register = template.Library()




@register.filter
def split(value, delimiter=","):
    """Split the string by delimiter."""
    return value.split(delimiter)

@register.filter
def get_item(dictionary, key):
    """Allows accessing a dictionary value by a variable key in templates."""
    return dictionary.get(key)

@register.filter
def at_index(list, index):
    """Allows accessing a list item by a variable index in templates."""
    if list and 0 <= index < len(list):
        return list[index]
    return None