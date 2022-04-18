import tensorflow as tf

dataset_path = 'C:/Users/Dominik/Desktop/niepsy/'
batch = 32
img_height = 180
img_width = 180
classes = 2
epochs = 15
save = True
where = 'C:/Users/Dominik/Desktop/isdog_model_xd'


def create_model():
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path,
        validation_split=0.2,
        subset='training',
        seed=123,
        color_mode='grayscale',
        image_size=(img_height, img_width),
        batch_size=batch)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_path,
        validation_split=0.2,
        subset="validation",
        seed=123,
        color_mode='grayscale',
        image_size=(img_height, img_width),
        batch_size=batch)

    AUTOTUNE = tf.data.AUTOTUNE

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    model = tf.keras.models.Sequential([
        tf.keras.layers.experimental.preprocessing.Rescaling(1. / 255, input_shape=(img_height, img_width, 1)),
        tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(2)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_ds, validation_data=val_ds, epochs=epochs)

    if save:
        model.save(where)

#create_model()
