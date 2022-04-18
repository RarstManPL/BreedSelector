from django.utils.translation import ugettext_lazy as _
from livesettings.functions import config_register
from livesettings.values import ConfigurationGroup, StringValue


BREEDSELECTOR_GROUP = ConfigurationGroup('BreedSelector_prediction', _('Prediction app settings '), ordering=0)

config_register(StringValue(
    BREEDSELECTOR_GROUP,
    'CHARACTER_MODEL',
    description=_('A model for predicting a dog character'),
    default="",
    ordering=1,
))

config_register(StringValue(
    BREEDSELECTOR_GROUP,
    'CHARACTER_HASH',
    description=_('LSHASH model to predict dog character'),
    default="",
    ordering=2,
))

config_register(StringValue(
    BREEDSELECTOR_GROUP,
    'ISDOG_MODEL',
    description=_('Model for determining if there is a dog in the photo '),
    default="",
    ordering=3,
))

config_register(StringValue(
    BREEDSELECTOR_GROUP,
    'LOOK_MODEL',
    description=_('Model for predicting a dog breed from a photo '),
    default="",
    ordering=4,
))
