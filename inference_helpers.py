from model_architecture import create_model


def inference_setup(Hz):
    model = create_model(Hz)
    model.load_weights("model.h5")
    return model


def downsample(audio_arr, curr_sample_rate, new_sample_rate):
    # To do: Downsample audio
    return audio_arr
