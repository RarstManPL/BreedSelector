from modeltranslation.translator import register, TranslationOptions
from .models import Category, Breed, Feature, Question, Choice


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['category_name']


@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ['feature_name']


@register(Breed)
class BreedTranslationOptions(TranslationOptions):
    fields = ['breed_name']


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ['question_text']


@register(Choice)
class ChoiceTranslationOptions(TranslationOptions):
    fields = ['choice_text']
