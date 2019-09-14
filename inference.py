from data_wrangling import get_windows_from_array
from inference_helpers import inference_setup, downsample
from librosa.core import load


Hz = 16000  # 16kHz. Will downsample audio to this rate.
model = inference_setup(Hz)


def classify(audio_file_path):
    audio_arr = load(audio_file_path, sr=Hz)
    overlap = 0
    windows = get_windows_from_array(audio_arr, Hz, overlap)
    windows = np.expand_dims(windows, axis=2)
    return model.predict(windows)
