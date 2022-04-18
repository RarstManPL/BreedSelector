import tensorflow as tf
import pandas
import pickle
import os
from livesettings.functions import config_value
from django.conf import settings
from ..models import Feature, Breed

from ...commons.util import round_down

model = tf.keras.models.load_model(
    os.path.join(settings.MEDIA_ROOT, config_value('BreedSelector_prediction', 'CHARACTER_MODEL')))
lsh = pickle.load(
    open(os.path.join(settings.MEDIA_ROOT, config_value('BreedSelector_prediction', 'CHARACTER_HASH')), 'rb'))

intermediate_layer_model = tf.keras.Model(inputs=model.input, outputs=model.get_layer('dense_1').output)

features = list(Feature.objects.exclude(feature_predictable=False).values_list('feature_code', flat=True))

lsh_hash = model.get_layer('dense_1').output.shape[1]
features_amount = len(features)
breeds_amount = len(Breed.objects.all())


def prepare_data(data_dict):
    return [int(data_dict[key]) if key in data_dict and int(data_dict[key]) in [0, 1, 2, 3] else 0 for key in
            features]


def normalize_data(prepared_data):
    dataframe = pandas.DataFrame({'Data': prepared_data})
    dataframe.replace(1, 0.333333, inplace=True)
    dataframe.replace(2, 0.666667, inplace=True)
    dataframe.replace(3, 1.000000, inplace=True)
    return dataframe


def predict(data_dict):
    prepared_data = prepare_data(data_dict)
    normalized_data = normalize_data(prepared_data)

    return {str(index): item for index, item in enumerate(
        [{'ID': extra_data, 'Percentage': round_down(100 - float(distance) * 100, 1)} for ((vec, extra_data), distance) in
         lsh.query(intermediate_layer_model.predict(normalized_data.to_numpy().reshape(1, features_amount)).reshape(1,
                                                                                                                    lsh_hash).flatten(),
                   num_results=breeds_amount, distance_func="centred_euclidean") if
         round_down(100 - float(distance) * 100, 1) > 0])}
