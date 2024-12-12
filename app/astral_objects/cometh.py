import requests
from .astral_object import AstralObject


class Cometh(AstralObject):
    """
    Represents a Cometh object, inheriting from the AstralObject class.

    A Cometh object has specific directions ('up', 'down', 'right', 'left')
    and can be posted or deleted at specified positions on a grid.
    """

    directions = ["up", "down", "right", "left"]

    def __init__(self, candidate_id):
        """
        Initialize a Cometh instance.

        Args:
            candidate_id (str): The unique identifier for the crossmint's candidate.
        """
        super().__init__(candidate_id)
        self.name = "Cometh"

    def post(self, rows_columns_tuple):
        """
        Post the Cometh object to a specified position with a given direction.

        Args:
            rows_columns_tuple (tuple): A tuple containing:
                - row (int): The row index where the Cometh should be posted.
                - column (int): The column index where the Cometh should be posted.
                - direction (str): The direction of the Cometh ('up', 'down', 'right', or 'left').

        Raises:
            AssertionError: If the tuple is not valid or the direction is not one of the allowed values.
            requests.exceptions.HTTPError: If the API request fails with an HTTP error.
            Exception: If any other unexpected error occurs.
        """
        self.check_tuples(rows_columns_tuple, 3, self.directions)
        url = "https://challenge.crossmint.io/api/comeths"
        headers = {"Content-Type": "application/json"}
        payload = {
            "candidateId": self.candidate_id,
            "row": rows_columns_tuple[0],
            "column": rows_columns_tuple[1],
            "direction": rows_columns_tuple[2],
        }

        response = requests.post(url, json=payload, headers=headers)
        try:
            response.raise_for_status()
            print("Success")
        except requests.exceptions.HTTPError as err:
            print("HTTP Error:", err)
            raise
        except Exception as err:
            print("An error occurred:", err)
            raise

    def delete(self, rows_columns_tuple):
        """
        Delete the Cometh object from a specified position.

        Args:
            rows_columns_tuple (tuple): A tuple containing:
                - row (int): The row index from which the Cometh should be deleted.
                - column (int): The column index from which the Cometh should be deleted.
        Raises:
            AssertionError: If the tuple is not valid.
            requests.exceptions.HTTPError: If the API request fails with an HTTP error.
            Exception: If an unexpected error occurs.
        """
        # self.check_tuples(rows_columns_tuple, 3, self.directions)
        self.check_tuples(rows_columns_tuple, 2)
        url = "https://challenge.crossmint.io/api/comeths"
        headers = {"Content-Type": "application/json"}
        payload = {
            "candidateId": self.candidate_id,
            "row": rows_columns_tuple[0],
            "column": rows_columns_tuple[1],
        }

        response = requests.delete(url, json=payload, headers=headers)
        try:
            response.raise_for_status()  # Raises HTTPError for bad responses
            print("Success")
        except requests.exceptions.HTTPError as err:
            print("HTTP Error:", err)
            raise
        except Exception as err:
            print("An error occurred:", err)
            raise
