import numpy as np
from sklearn.metrics import mean_squared_error


class MSE:

    def __init__(self, target_image_array: np.ndarray):
        self.target_image_array = target_image_array

    def compute_mean_squared_error(self, individual_array: np.ndarray) -> float:
        """
        TBD
        :return:
        """
        mse = mean_squared_error(self.target_image_array, individual_array)
        return mse
