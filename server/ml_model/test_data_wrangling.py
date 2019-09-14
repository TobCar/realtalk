import numpy as np
from ml_model.data_wrangling import get_windows_from_array


def test_get_windows_from_array():
    arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    windows = get_windows_from_array(arr, 4, 0.25)
    assert (windows == np.array([[1,2,3,4], [4,5,6,7]])).all()
