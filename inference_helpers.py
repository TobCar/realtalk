from model_architecture import create_model


def inference_setup(Hz):
    model = create_model(Hz)
    model.load_weights("model.h5")
    return model

def round_predictions(predictions):
    return int(round((sum(predictions)[0]) / len(predictions)))
