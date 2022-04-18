import io
import os

import pandas
import tensorflow as tf
from PIL import Image, ImageOps
from django.conf import settings
from keras_preprocessing import image
from livesettings.functions import config_value
from pandas import np

from ...commons.util import round_down

look_model = tf.keras.models.load_model(
    os.path.join(settings.MEDIA_ROOT, config_value('BreedSelector_prediction', 'LOOK_MODEL')))

isdog_model = tf.keras.models.load_model(
    os.path.join(settings.MEDIA_ROOT, config_value('BreedSelector_prediction', 'ISDOG_MODEL')))


def is_dog(img):
    score = tf.nn.softmax(isdog_model.predict(
        tf.expand_dims(image.img_to_array(ImageOps.grayscale(img.resize((180, 180), Image.NEAREST))), 0))[0])
    return {'IsDog': True, 'IsDogScore': 100 * np.max(score)} if np.argmax(score) == 0 else {}


def predict(images):
    prediction_list = []
    amount_not_dog = 0
    skiped_due_to_error = 0

    for image_data in images:
        try:
            img = Image.open(io.BytesIO(image_data.read()))

            if not is_dog(img):
                amount_not_dog += 1
                continue

            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            data[0] = (np.asarray(ImageOps.fit(img, (224, 224), Image.ANTIALIAS)).astype(np.float32) / 127.0) - 1

            prediction_list.append({index + 1: round_down(float(possibility) * 100, 1) for index, possibility in
                                    enumerate(look_model.predict(data)[0])})
        except Exception:
            skiped_due_to_error += 1
            continue

    parsed_dict = {}
    dataframe = []

    for index, prediction in enumerate(prediction_list):
        parsed_dict[index] = {key: value for key, value in sorted(
            {key: value for key, value in prediction.items() if
             value > 0}.items(), key=lambda item: item[1], reverse=True)}
        dataframe.append(parsed_dict[index])

    parsed_dict['Sum'] = {key: round_down(float(value), 1) for key, value in dict(pandas.DataFrame(dataframe).mean()).items()}
    parsed_dict['Output'] = {
        'AmountDog': len(prediction_list),
        'AmountNotDog': amount_not_dog,
        'SkippedDueToError': skiped_due_to_error
    }

    return parsed_dict
