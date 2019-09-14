from ml_model.data_wrangling import get_windows_from_array
from ml_model.inference_helpers import inference_setup, round_predictions
from pydub import AudioSegment
import numpy as np


Hz = 16000  # 16kHz. Will downsample audio to this rate.
model = inference_setup(Hz)


def classify(audio_file_path):
    """
    :param audio_file_path: Path to an mp3 file.
    :return: Array of 1 second values. Each entry in the array is whether that second is a real voice or not.
    """
    # We assume the mp3 file has 16 bits per sample so there are 16,000 samples in a second.
    audio_arr = np.array(AudioSegment.from_mp3(audio_file_path).get_array_of_samples())
    overlap = 0
    windows = get_windows_from_array(audio_arr, Hz, overlap)
    windows = np.expand_dims(windows, axis=2)
    output = []
    for window in windows:
        window = np.reshape(window, (1, window.shape[0], window.shape[1]))
        predictions = model.predict(window)
        output.append(round_predictions(predictions))
    return output
