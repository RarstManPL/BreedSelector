from django import template

from apps.commons.models import Category, Question

register = template.Library()


@register.filter(name='get_visible')
def get_visible(queryset, is_visible):
    return queryset.filter(**{queryset.model.__name__.lower() + '_visible': is_visible})


@register.filter(name='get_profitable_categories')
def get_profitable_categories(category_queryset=Category.objects.all()):
    return category_queryset.filter(
        category_visible=True
    ).filter(
        feature__feature_predictable=True,
        feature__question__question_visible=True
    ).distinct()


@register.filter(name='get_profitable_questions')
def get_profitable_questions(category):
    return Question.objects.all().filter(
        feature__category=category,
        question_visible=True,
        feature__feature_predictable=True
    )


@register.filter(name='replace')
def replace(value, args):
    args = args.split(sep=";", maxsplit=2)
    return str(value).replace(args[0], args[1])
