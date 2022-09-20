from django import template


register = template.Library()

@register.filter()
def censor(value):
    block_list = ('редиска', 'бяка', 'бука', 'Россия', 'Китай')
    text = value.split()
    after_censorship = []
    text = list(text)
    return f'{value}'