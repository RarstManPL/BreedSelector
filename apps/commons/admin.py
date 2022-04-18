from .models import Category, Feature, Breed, FeatureValue, Question, Choice
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ChoiceInLine(SortableInlineAdminMixin, admin.TabularInline):
    model = Choice
    extra = 0


class FeatureValueInLine(admin.TabularInline):
    model = FeatureValue
    extra = 0


@admin.register(Category)
class CategoryAdminModel(SortableAdminMixin, admin.ModelAdmin):
    fieldsets = [
        (_('Category settings'), {'fields': ['category_name']}),
        (_('Visibility settings'), {'fields': ['category_visible']})
    ]
    list_filter = ['category_visible']
    list_display = ['category_name', 'category_visible']


@admin.register(Feature)
class FeatureAdminModel(admin.ModelAdmin):
    fieldsets = [
        (_('Feature settings'), {'fields': ['feature_name', 'feature_code']}),
        (_('Category settings'), {'fields': ['category']}),
        (_('Sensitive settings (! SELECT ONLY WHEN THE MODEL SUPPORTS THIS FEATURE !)'), {'fields': ['feature_predictable']})
    ]
    list_filter = ['category', 'feature_predictable']
    list_display = ['feature_name', 'feature_code', 'category', 'feature_predictable']


@admin.register(Breed)
class BreedAdminModel(admin.ModelAdmin):
    fieldsets = [
        (_('Breed settings'), {'fields': ['breed_name']}),
        (_('Breed image'), {'fields': ['breed_image']}),
        (_('Visibility settings'), {'fields': ['breed_visible']})
    ]
    inlines = [FeatureValueInLine]
    list_filter = ['breed_visible']
    list_display = ['breed_name', 'breed_visible']
    search_fields = ['breed_name']


@admin.register(Question)
class QuestionAdminModel(SortableAdminMixin, admin.ModelAdmin):
    fieldsets = [
        (_('Question settings'), {'fields': ['question_text']}),
        (_('Feature settings'), {'fields': ['feature']}),
        (_('Visibility settings'), {'fields': ['question_visible']})
    ]
    inlines = [ChoiceInLine]
    list_filter = ['feature__category', 'question_visible']
    list_display = ['question_text', 'feature', 'question_visible']
