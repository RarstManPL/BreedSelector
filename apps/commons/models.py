from django.db import models
from .fields import IntegerRangeField


class Category(models.Model):
    category_name = models.CharField(max_length=300)
    category_order = IntegerRangeField(default=0, min_value=0)
    category_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    class Meta(object):
        ordering = ['category_order']


class Feature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=300)
    feature_code = models.CharField(max_length=50, unique=True)
    feature_predictable = models.BooleanField(default=False)

    def __str__(self):
        return self.feature_name


def breed_name_based_upload_to(instance, filename):
    return "breeds/{0}/{1}".format(instance.breed_name, filename)


class Breed(models.Model):
    breed_name = models.CharField(max_length=300)
    breed_features = models.ManyToManyField(Feature)
    breed_image = models.ImageField(default='no_image.png', upload_to=breed_name_based_upload_to)
    breed_info_url = models.URLField(default='https://wamiz.pl/pies/rasy')
    breed_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.breed_name


class FeatureValue(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    feature_value = IntegerRangeField(min_value=1, max_value=3, default=1)

    class Meta:
        unique_together = ('breed', 'feature')


class Question(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, unique=True)
    question_order = IntegerRangeField(default=0, min_value=0)
    question_text = models.CharField(max_length=300)
    question_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text

    class Meta(object):
        ordering = ['question_order']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    choice_value = IntegerRangeField(default=1, min_value=1, max_value=3)
    choice_order = IntegerRangeField(default=0, min_value=0)
    choice_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.choice_text

    class Meta(object):
        ordering = ['choice_order']
