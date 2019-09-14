from tf.keras.layers import MaxPooling, Conv1D, BatchNormalization, Dense, Dropout
from tf.keras import Sequential


def create_model():
    model = Sequential()

    # 1D Convolutional Layers, first two blocks include max pooling
    model.add(Conv1D(16, kernel_size=64, strides=2, input_shape=(compound_image_size, compound_image_size, number_of_channels), activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling(pool_size=8, strides=8))

    model.add(Conv1D(32, kernel_size=32, strides=2, activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling(pool_size=8, strides=8))

    model.add(Conv1D(64, kernel_size=16, strides=2, activation="relu"))
    model.add(BatchNormalization())

    model.add(Conv1D(128, kernel_size=8, strides=2, activation="relu"))
    model.add(BatchNormalization())

    # Fully connected layers
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.25))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.25))
    model.add(Dense(1, activation="sigmoid"))
