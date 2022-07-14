import csv
import os
from datetime import datetime
from typing import Optional

from models.constellation import Constellation


class SaveResults:

    def __init__(
            self,
            experiment_name: str,
            count_vertices: int,
            save_freq: int,
            target_image_name: str,
            algo_name: str
    ) -> None:
        self.experiment_name = experiment_name
        self.count_vertices = count_vertices
        self.save_freq = save_freq
        self.target_image_name = target_image_name
        self.algo_name = algo_name
        self.results_directory = f"results/{self.experiment_name}_{self.algo_name}"
        self.img_directory = f"img/temp/{self.experiment_name}_{self.target_image_name}_{self.algo_name}"

    def save_csv(
            self,
            iteration: int,
            average_mse: float,
            average_fitness: Optional[str] = None,
            simulated_annealing: Optional[int] = None
    ) -> None:
        """
        Save results to csv file.
        :param average_fitness: Average fitness of the population.
        :param average_mse: Average MSE of the population.
        :param iteration: Which iteration is being saved.
        :param simulated_annealing: Whether the new individual is being generated using simulated annealing.
        :return: None
        """

        now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")

        row = [iteration, str(average_fitness), average_mse, str(simulated_annealing), now]

        if not os.path.exists(self.results_directory):
            os.mkdir(self.results_directory)

        if f"results_{self.target_image_name}.csv" not in os.listdir(self.results_directory + "/"):
            with open(self.results_directory + f"/results_{self.target_image_name}.csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Iteration", "Average fitness", "Average MSE", "Simulated annealing", "Time"])
                writer.writerow(row)

        else:
            with open(self.results_directory + f"/results_{self.target_image_name}.csv", "a") as csv_file:
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
