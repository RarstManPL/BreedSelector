import os
import pickle
import time

import lshashpy3 as lshash
import numpy as np
import pandas
import tensorflow as tf
from django.conf import settings
from sklearn import preprocessing

from ...models import Breed, Feature

fake_dogs = 200
train_proportion = 0.8
batch = 64
epochs = 7000
path_model = os.path.join(settings.MEDIA_ROOT, 'generated_models/character/')
path_lsh = os.path.join(settings.MEDIA_ROOT, 'generated_models/character_lsh/')

features = list(Feature.objects.exclude(feature_predictable=False).values_list('feature_code', flat=True))


def load_data():
    dataframe = pandas.DataFrame().from_records(list(
        Breed.objects.all().values('id', 'breed_name', 'featurevalue__feature_value',
                                   'featurevalue__feature__feature_code')))
    dataframe = dataframe.pivot(columns='featurevalue__feature__feature_code', index=['id', 'breed_name'])
    dataframe = dataframe.droplevel(0, axis=1).reset_index()

    columns_stay = ['id', 'breed_name']
    columns_stay.extend(features)

    dataframe = dataframe.drop(dataframe.columns.difference(columns_stay))
    dataframe = dataframe.dropna(subset=features)
    dataframe = dataframe.reindex(columns=columns_stay)

    return dataframe


def make_fake_dog(_vector):
    vector = _vector.copy()
    vector_copy = vector[vector.columns.difference(['breed_name', 'id'])]
    random_column = vector_copy.sample(axis='columns')
    random_column_value = int(vector_copy[random_column.columns[0]])
    vector[random_column.columns[0]] = random_column_value - 1 if random_column_value > 0 else random_column_value + 1
    return vector


def create_model():
    dataFrame = load_data()

    for i in range(0, 100):
        dataFrame = dataFrame.append(make_fake_dog(dataFrame.sample()))

    values = dataFrame[dataFrame.columns.difference(['breed_name', 'id'], sort=False)]
    names = dataFrame.columns.difference(['breed_name', 'id'], sort=False)

    scaled_minMax = pandas.DataFrame(preprocessing.MinMaxScaler().fit_transform(values), columns=names)

    train_scale = int(train_proportion * len(scaled_minMax))

    training_set = scaled_minMax[0:train_scale]
    _training_labels = dataFrame['id'][0:train_scale]

    training_labels = []
    unique = _training_labels.nunique()
    _training_labels = _training_labels.to_numpy()

    for i in range(0, len(_training_labels)):
        tmp = [0] * unique
        tmp[_training_labels[i] - 1] = 1
        training_labels.append(tmp)

    test_set = scaled_minMax[train_scale - 1:-1]
    _test_labels = dataFrame['id'][train_scale - 1:-1].to_numpy()

    test_labels = []
    for i in range(0, len(_test_labels)):
        tmp = [0] * unique
        tmp[_test_labels[i] - 1] = 1
        test_labels.append(tmp)

    test_labels = np.array(test_labels)
    training_labels = np.array(training_labels)

    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=scaled_minMax.shape[1]),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dense(48, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(unique, activation='relu'),
        tf.keras.layers.Softmax()
    ])

    model.compile(optimizer='adam', loss=tf.keras.losses.MeanSquaredError(), metrics=['accuracy'])
    model.fit(training_set, training_labels, epochs=epochs, batch_size=batch)
    test_loss, test_acc = model.evaluate(test_set, test_labels, verbose=2)

    intermediate_layer_model = tf.keras.Model(inputs=model.input, outputs=model.get_layer('dense_1').output)
    lsh = lshash.LSHash(1, model.get_layer('dense_1').output.shape[1])

    for i in range(0, scaled_minMax.shape[0]):
        lsh.index(intermediate_layer_model.predict(scaled_minMax.iloc[i].to_numpy().reshape(1, len(features)))[0],
                  dataFrame['id'].iloc[i])

    time_mills = round(time.time() * 1000)

    model.save(os.path.join(path_model, 'character_' + str(time_mills) + '/'))

    lsh_filename = os.path.join(path_lsh, 'character_lsh_' + str(time_mills) + ".p")

    if not os.path.exists(os.path.dirname(lsh_filename)):
        os.makedirs(os.path.dirname(lsh_filename))

    with open(lsh_filename, 'wb') as handle:
        pickle.dump(lsh, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return [test_loss, test_acc, time_mills]
