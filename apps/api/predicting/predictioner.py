import time

from ..models import Feature
from .characterpredicting import predict as predict_character
from .imagepredicting import predict as predict_images

features = list(Feature.objects.exclude(feature_predictable=False).values_list('feature_code', flat=True))


class Predictioner(object):
    def __init__(self, POST, FILES):
        self.POST = prepare_data_to_character_predict(POST)
        self.FILES = FILES
        self.predict_character = len(self.POST) >= 1
        self.predict_images = len(self.FILES) >= 1
        self.predicted_character = []
        self.predicted_images = []

        if self.predict_character:
            self.predicted_character = predict_character(self.POST)

        if self.predict_images:
            self.predicted_images = predict_images(self.FILES)

    def get_prediction(self):
        while (self.predict_character and not self.predicted_character) or (
                self.predict_images and not self.predicted_images):
            time.sleep(0.5)

        return {'Character': self.predicted_character if self.predict_character else {},
                'Images': self.predicted_images if self.predict_images else {}}


def prepare_data_to_character_predict(POST):
    POST = dict(POST.lists())
    return {key: int(POST[key][0]) for key in features if key in POST}
