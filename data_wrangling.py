import numpy as np
import pandas as pd
import soundfile as sf


def load_labels_df():
    """
    Example usage: `load_labels_df().loc["PA_E_0133778"]["LABEL"]` to get the label for file PA_E_0133778.flac
    :return: DataFrame with the audio file name as the index and the label as the column LABEL.
    """
    file_loc = "ASVspoof2019_PA_real/ASVspoof2019_PA_cm_protocols/ASVspoof2019.PA.real.cm.eval.trl.txt"
    df = pd.read_csv(file_loc, delimiter="\t")[:2699]  # We have 2700 files, ignore extra blank line at end
    df["LABEL"] = df["LABEL"].apply(lambda s: s == "bonafide")
    relevant_df = df[["AUDIO_FILE_NAME", "LABEL"]]
    relevant_df.set_index("AUDIO_FILE_NAME", inplace=True)
    return relevant_df


def calculate_class_weights(labels_df):
    """
    :param labels_df: Data Frame with the column "LABEL"
    :return: Class weights
    """
    real = len(labels_df[labels_df["LABEL"] == 1])
    fake = len(labels_df[labels_df["LABEL"] == 0])
    return {1: fake / real, 0: real / fake}


def get_windows_from_array(arr, values_per_window, overlap):
    """
    :param arr: Array to split up
    :param values_per_window: Values per window.
    :param overlap: Percent overlap between windows. Determines how much the window moves.
    :return: 2D array.
    """
    stride = int(values_per_window * (1 - overlap))
    output = []
    left = 0
    right = values_per_window
    while right <= len(arr):
        output.append(arr[left:right])
        left += stride
        right += stride
    return np.array(output)


def random_split(df):
    train_percent = 0.80
    validation_percent = 0.10

    perm = np.random.permutation(df.index)
    m = len(df)
    train_end = int(train_percent * m)
    validate_end = int(validation_percent * m) + train_end
    train = df.loc[perm[:train_end]]
    validate = df.loc[perm[train_end:validate_end]]
    test = df.loc[perm[validate_end:]]
    return train, validate, test


def split_data(labels_df):
    true_split = random_split(labels_df[labels_df["LABEL"] == 1])
    false_split = random_split(labels_df[labels_df["LABEL"] == 0])

    training = pd.concat([true_split[0], false_split[0]], axis=0)
    validation = pd.concat([true_split[1], false_split[1]], axis=0)
    testing = pd.concat([true_split[2], false_split[2]], axis=0)

    return training, validation, testing


def windows_for_each_file_labels_split(labels_df, values_per_window, overlap):
    output_x = np.empty((0, values_per_window))
    output_y = []
    print("Creating windows (separate X and Y arrays)...")
    for index, row in labels_df.iterrows():
        print("Processing {}".format(index))
        label = row["LABEL"]
        filename_w_extension = index + ".flac"
        path = "ASVspoof2019_PA_real/ASVspoof2019_PA_real/flac/{}".format(filename_w_extension)
        data, sample_rate = sf.read(path)
        windows = get_windows_from_array(data, values_per_window, overlap)
        output_x = np.append(output_x, windows, axis=0)
        output_y += [label] * windows.shape[0]

    output_x = np.reshape(output_x, (output_x.shape[0], output_x.shape[1], 1))
    output_y = np.array(output_y)
    output_y = np.reshape(output_y, (output_y.shape[0], 1))

    return output_x, output_y
