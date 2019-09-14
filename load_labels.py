import pandas as pd


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
