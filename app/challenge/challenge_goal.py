import os
import time
import logging
import requests

from dotenv import load_dotenv
from .class_identifier import ClassIdentifier


load_dotenv()
logger = logging.getLogger(__name__)


class ChallengeGoal:
    """
    A class to manage and solve the challenges provided by crossmint by interacting with a goal map.

    The `ChallengeGoal` class retrieves a goal map and identifies
    and instantiates objects to solve the specified challenges. It includes
    mechanisms for retrying API requests when rate-limited.
    """

    def __init__(self):
        """
        Initializes a ChallengeGoal instance.

        Attributes:
            class_id (ClassIdentifier or None): The ClassIdentifier instance used for dynamic class discovery.
            classes (dict or None): A dictionary of discovered classes.
            goal_map (list or None): The retrieved goal map representing the challenge to solve.
            candidate_id (str): Thecrossmint's candidate id loaded from the environment.
            initialized (dict): A dictionary of initialized objects by their class names.
        """
        self.class_id = None
        self.classes = None
        self.goal_map = None
        self.candidate_id = os.getenv("CANDIDATE_ID")
        self.initialized = {}

    def get_goal_map(self):
        """
        Retrieve the goal map from the external API.

        Sends a GET request to fetch the goal map for the current candidate.

        Returns:
            list: The retrieved goal map.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returns an error.
            Exception: For other issues that may occur during the request.
        """
        url = f"https://challenge.crossmint.io/api/map/{self.candidate_id}/goal"
        try:
            response = requests.get(url)
            response.raise_for_status()

            goal_map = response.json()
            print("Goal Map Retrieved Successfully:", goal_map)
            self.goal_map = goal_map["goal"]
            return self.goal_map
        except requests.exceptions.HTTPError as err:
            print("HTTP Error:", err)
            raise
        except Exception as err:
            print("An error occurred:", err)
            raise

    def solve_challengue_1(self, max_ret=5):
        """
        Solve Challenge 1 by posting objects based on the goal map.

        Iterates through the goal map, identifies corresponding objects ('SPACE' or 'POLYANET'), and posts
        them to the API. Implements retry logic for handling rate-limited requests.

        Args:
            max_ret (int, optional): Maximun number of tries.
        Raises:
            Exception: If an item fails to post after the maximum retries.
        """
        self.class_id = ClassIdentifier()
        self.classes = self.class_id.get_class_info()
        max_retries = max_ret
        for row_index, row in enumerate(self.goal_map):
            for col_index, item in enumerate(row):
                if item.lower() in self.classes:
                    if item.lower() not in self.initialized:
                        item_def = self.class_id.create_instance(
                            item.lower(), candidate_id=self.candidate_id
                        )
                        self.initialized[item.lower()] = item_def
                    # print(item.lower())
                    # self.initialized[item.lower()].post((row_index, col_index))
                    for attempt in range(max_retries):
                        try:
                            logger.info(
                                f"Posting item '{item.lower()}' at position ({row_index}, {col_index})"
                            )
                            self.initialized[item.lower()].post((row_index, col_index))
                            break  # Exit retry loop on success
                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 429:
                                wait_time = 2**attempt
                                logger.warning(
                                    f"Rate limit reached. Retrying in {wait_time} seconds..."
                                )
                                time.sleep(wait_time)
                            else:
                                logger.error(f"HTTP Error occurred: {e}")
                                raise
                        except Exception as e:
                            logger.error(f"An unexpected error occurred: {e}")
                            raise
                    else:
                        logger.error(
                            f"Failed to post item '{item.lower()}' after {max_retries} retries."
                        )
                        raise Exception(
                            "Max retries exceeded for rate-limited requests."
                        )

    def solve_challengue_2(self, max_ret=5):
        """
        Solve Challenge 2 by posting objects with optional attributes based on the goal map.

        Iterates through the goal map, identifies corresponding objects, and posts
        them to the API. If an item contains an attribute (e.g., colors or directions),
        it is included in the post request. Implements retry logic for handling rate-limited requests.

        Args:
            max_ret (int, optional): Maximun number of tries.

        Raises:
            Exception: If an item fails to post after the maximum retries.
        """
        self.class_id = ClassIdentifier()
        self.classes = self.class_id.get_class_info()
        max_retries = max_ret
        for row_index, row in enumerate(self.goal_map):
            for col_index, item in enumerate(row):
                if "_" in item:
                    attribute, name = [x.lower() for x in item.split("_")]
                else:
                    attribute, name = [None, item.lower()]
                if name in self.classes:
                    if name not in self.initialized:
                        item_def = self.class_id.create_instance(
                            name, candidate_id=self.candidate_id
                        )
                        self.initialized[name] = item_def
                    # print(item.lower())
                    # self.initialized[item.lower()].post((row_index, col_index))
                    for attempt in range(max_retries):
                        try:
                            if attribute:
                                logger.info(
                                    f"Posting item '{name}' at position ({row_index}, {col_index}) with attribute {attribute}"
                                )
                                self.initialized[name].post(
                                    (row_index, col_index, attribute)
                                )
                            else:
                                logger.info(
                                    f"Posting item '{name}' at position ({row_index}, {col_index})"
                                )
                                self.initialized[name].post((row_index, col_index))
                            break  # Exit retry loop on success
                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 429:
                                wait_time = 2**attempt
                                logger.warning(
                                    f"Rate limit reached. Retrying in {wait_time} seconds..."
                                )
                                time.sleep(wait_time)
                            else:
                                logger.error(f"HTTP Error occurred: {e}")
                                raise
                        except Exception as e:
                            logger.error(f"An unexpected error occurred: {e}")
                            raise
                    else:
                        logger.error(
                            f"Failed to post item '{name}' after {max_retries} retries."
                        )
                        raise Exception(
                            "Max retries exceeded for rate-limited requests."
                        )
