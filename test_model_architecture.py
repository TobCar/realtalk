import mltest
from model_architecture import create_model
import tensorflow as tf
import numpy as np


def setup():
    np.random.seed(42)  # Test input is randomly generated so we need a seed for consistent testing
    mltest.setup()


def test_model_architecture():
    Hz = 16000  # 16kHz

    # Make the model input a placeholder
    input_tensor = tf.placeholder(tf.float32, (None))
    label_tensor = tf.placeholder(tf.int32, (None))

    # Build the model
    model = create_model(Hz)

    # Give the model some random input
    feed_dict = {
      input_tensor: np.random.normal(size=(Hz)),
      label_tensor: np.random.randint((Hz))
    }

    # Run the test suite
    mltest.test_suite(
        model.prediction,
        model.train_op,
        feed_dict=feed_dict,
        output_range=(0, 1))
