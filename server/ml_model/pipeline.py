from ml_model.data_wrangling import load_labels_df, calculate_class_weights, split_data, windows_for_each_file_labels_split, windows_for_each_file_labels_together
from mml_model.odel_architecture import create_model
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.optimizers import Adadelta
from tensorflow.keras.metrics import binary_accuracy
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.callbacks import EarlyStopping


# Seed for reproducible data splits
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(42)

# Make TensorFlow use one thread, multiple threads are a source of unpredictability
session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
from keras import backend as K
tf.set_random_seed(42)
sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)

# Define hyperparameters
Hz = 16000  # 16kHz. Our dataset is all in 16kHz so we won't need to worry about downsampling during training!
values_per_window = Hz
overlap = 0.50

batch_size = 100
epochs = 100  # Early stopping will likely stop training before 100 epochs run

# Load and split the data
print("Loading the data...")
labels_df = load_labels_df()
training_df, validation_df, testing_df = split_data(labels_df)
training_x, training_y = windows_for_each_file_labels_split(training_df, values_per_window, overlap)
validation = windows_for_each_file_labels_split(validation_df, values_per_window, overlap)
print("Loaded the data.")

# Calculate class weights based on the training data to avoid information leakage
class_weights = calculate_class_weights(training_df)

# Create the model
print("Creating the model...")
model = create_model(Hz)
model.compile(optimizer=Adadelta(lr=1.0), loss=binary_crossentropy, metrics=[binary_accuracy])
print("Created the model.")

# Train the model with early stopping
print("Training the model...")
early_stopping = EarlyStopping("val_loss", patience=5, restore_best_weights=True)
callbacks_list = [early_stopping]

model.fit(training_x, training_y, epochs=epochs, validation_data=validation, shuffle=True, callbacks=callbacks_list)

print("Finished training the model!")

print("Saving model weights...")
model.save_weights("model.h5")
print("Saved model weights.")

print("Splitting up test data into windows.")
testing_x, testing_y = windows_for_each_file_labels_split(testing_df, values_per_window, overlap)
print("Split test data into windows.")

print("Evaluating on the test set...")
output = model.evaluate(testing_x, testing_y, batch_size=batch_size)
print("Evaluated on the test set! Metrics:")
for i, metric_name in enumerate(model.metrics_names):
    print(metric_name + " " + str(output[i]))
