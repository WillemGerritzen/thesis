import csv
import os
from datetime import datetime
from typing import List

from models.constellation import Constellation


class SaveResults:

    def __init__(self, experiment_name: str, count_vertices: int, save_freq: int, target_image_name: str) -> None:
        self.experiment_name = experiment_name
        self.count_vertices = count_vertices
        self.save_freq = save_freq
        self.target_image_name = target_image_name

    def save_csv(self, iteration: int, average_fitness: float, average_mse: float) -> None:
        """
        Save results to csv file.
        :param average_fitness: Average fitness of the population.
        :param average_mse: Average MSE of the population.
        :param iteration: Which iteration is being saved.
        :return: None
        """

        now = datetime.now().strftime("%H:%M:%S %d-%m-%Y")

        row = [iteration, average_fitness, average_mse, now]

        if not os.path.exists(f"results/{self.experiment_name}_{self.count_vertices}"):
            os.mkdir(f"results/{self.experiment_name}_{self.count_vertices}")

        if f"results_{self.target_image_name}.csv" not in os.listdir(f"results/{self.experiment_name}_{self.count_vertices}/"):
            with open(f"results/{self.experiment_name}_{self.count_vertices}/results_{self.target_image_name}.csv", "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Iteration", "Average fitness", "Average MSE", "Time"])
                writer.writerow(row)

        else:
            with open(f"results/{self.experiment_name}_{self.count_vertices}/results_{self.target_image_name}.csv", "a") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(row)

    def save_images(self, iteration: int, population: List[Constellation]) -> None:
        """
        Save the current population to an image.
        :param iteration: Which iteration is being saved.
        :param population: The population to be saved.
        :return: None
        """

        if not os.path.exists(f"img/temp/{self.experiment_name}_{self.target_image_name}_{iteration}"):
            os.mkdir(f"img/temp/{self.experiment_name}_{self.target_image_name}_{iteration}")

        for individual in population:
            individual.individual_as_image.save(
                f"img/temp/{self.experiment_name}_{self.target_image_name}_{iteration}/{population.index(individual)}.bmp",
                "bmp"
            )
