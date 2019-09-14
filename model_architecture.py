from tensorflow.keras.layers import Input, MaxPool1D, Conv1D, BatchNormalization, Dense, Dropout, Flatten
from tensorflow.keras import Model


def create_model(samples):
    inputs = Input((samples, 1))

    # 1D Convolutional Layers, first two blocks include max pooling
    X = Conv1D(16, kernel_size=64, strides=2, activation="relu")(inputs)
    X = BatchNormalization()(X)
    X = MaxPool1D(pool_size=8, strides=8)(X)

    X = Conv1D(32, kernel_size=32, strides=2, activation="relu")(X)
    X = BatchNormalization()(X)
    X = MaxPool1D(pool_size=8, strides=8)(X)

    X = Conv1D(64, kernel_size=16, strides=2, activation="relu")(X)
    X = BatchNormalization()(X)

    X = Conv1D(128, kernel_size=8, strides=2, activation="relu")(X)
    X = BatchNormalization()(X)

    # Fully connected layers
    X = Flatten()(X)
    X = Dense(128, activation="relu")(X)
    X = Dropout(rate=0.25)(X)
    X = Dense(64, activation="relu")(X)
    X = Dropout(rate=0.25)(X)
    outputs = Dense(1, activation="sigmoid")(X)

    model = Model(inputs=inputs, outputs=outputs)

    return model
