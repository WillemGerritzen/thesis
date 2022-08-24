import csv
import os
import pickle
from datetime import datetime
from typing import Optional

from models.constellation import Constellation


class SaveResults:

    def __init__(
            self,
            run_number: str,
            count_vertices: int,
            save_freq: int,
            target_image_name: str,
            algo_name: str,
            ffa: bool
    ) -> None:
        self.run_number = run_number
        self.count_vertices = count_vertices
        self.save_freq = save_freq
        self.target_image_name = target_image_name
        self.algo_name = algo_name
        self.log_directory = f"dump/log/{self.count_vertices}/{self.run_number}_{self.algo_name}/" if not ffa else f"dump/log/{self.count_vertices}/{self.run_number}_{self.algo_name}_ffa/"
        self.img_directory = f"dump/img/{self.count_vertices}/{self.run_number}_{self.target_image_name}_{self.algo_name}/" if not ffa else f"dump/img/{self.count_vertices}/{self.run_number}_{self.target_image_name}_{self.algo_name}_ffa/"

    def save_csv(
            self,
            iteration: int,
            average_mse: float,
            average_fitness: Optional[str] = None,
            simulated_annealing: Optional[int] = None,
            best_fitness: Optional[str] = None,
            best_mse: Optional[float] = None
    ) -> None:
        """
        Save dump to csv file.
        :param best_mse: Best fitness in the current population.
        :param best_fitness: Best MSE in the current population.
        :param average_fitness: Average fitness of the population.
        :param average_mse: Average MSE of the population.
        :param iteration: Which iteration is being saved.
        :param simulated_annealing: Whether the new individual is being generated using simulated annealing.
        :return: None
        """

        now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")

        row = [iteration, str(average_fitness), average_mse, str(simulated_annealing), str(best_fitness), str(best_mse), now]

        if not os.path.exists(self.log_directory):
            os.mkdir(self.log_directory)

        if f"results_{self.target_image_name}.csv" not in os.listdir(self.log_directory):
            with open(self.log_directory + f"/results_{self.target_image_name}.csv", "w", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Iteration", "Average fitness", "Average MSE", "Simulated annealing", "Best fitness", "Best MSE", "Time"])
                writer.writerow(row)

        else:
            with open(self.log_directory + f"/results_{self.target_image_name}.csv", "a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(row)

    def save_images(self, iteration: int, individual: Constellation) -> None:
        """
        Save the current population to an image.
        :param iteration: Which iteration is being saved.
        :param individual: The individual to be saved.
        :return: None
        """

        if not os.path.exists(self.img_directory):
            os.mkdir(self.img_directory)

        individual.individual_as_image.save(self.img_directory + f"/{iteration}.png", 'png')

    def save_pickle(self, mapping: dict) -> None:
        """
        Save the current population to a pickle file.
        :param mapping: The mapping to be saved.
        :return: None
        """

        if not os.path.exists(self.log_directory):
            os.mkdir(self.log_directory)

        lst = []
        for key, value in mapping.items():
            for _ in value:
                lst.append(key)


        with open(self.log_directory + f"/list_{self.target_image_name}.pkl", "wb") as f:
            pickle.dump(lst, f)
