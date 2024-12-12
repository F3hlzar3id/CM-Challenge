import unittest

from unittest.mock import patch, Mock
import requests
from app.astral_objects.polyanet import Polyanet


class TestPolyanet(unittest.TestCase):
    """
    Test suite for the Polyanet class.

    This test suite verifies the behavior of the Polyanet class, including:
    - Successful posting and deletion of Polyanet objects.
    - Handling HTTP errors during API interactions.
    """

    def setUp(self):
        """
        Set up a Polyanet instance with a mock candidate ID for testing.
        """
        self.polyanet = Polyanet(candidate_id="123")

    @patch("app.astral_objects.polyanet.requests.post")
    def test_post_success(self, mock_post):
        """
        Test successful posting of a Polyanet object.

        Simulates a 200 OK response from the API when posting a Polyanet object,
        and verifies that the correct parameters are sent in the API request.
        """
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.raise_for_status = Mock()

        # Test the post method
        self.polyanet.post((1, 2))
        mock_post.assert_called_once_with(
            "https://challenge.crossmint.io/api/polyanets",
            json={"candidateId": "123", "row": 1, "column": 2},
            headers={"Content-Type": "application/json"},
        )

    @patch("app.astral_objects.polyanet.requests.post")
    def test_post_http_error(self, mock_post):
        """
        Test handling of an HTTP error during a POST request.

        Simulates a 404 Not Found response from the API when posting a Polyanet object,
        and verifies that the method raises an HTTPError.
        """
        # Configure the mock to simulate an HTTP error
        mock_post.return_value = Mock(status_code=404)
        mock_post.return_value.raise_for_status = Mock(
            side_effect=requests.exceptions.HTTPError("404 Error")
        )

        # Test the post method
        with self.assertRaises(requests.exceptions.HTTPError):
            self.polyanet.post((1, 2))

    @patch("app.astral_objects.polyanet.requests.delete")
    def test_delete_success(self, mock_delete):
        """
        Test successful deletion of a Polyanet object.

        Simulates a 200 OK response from the API when deleting a Polyanet object,
        and verifies that the correct parameters are sent in the API request.
        """
        # Configure the mock to simulate a successful API response
        mock_delete.return_value = Mock(status_code=200)
        mock_delete.return_value.raise_for_status = Mock()

        # Test the delete method
        self.polyanet.delete((1, 2))
        mock_delete.assert_called_once_with(
            "https://challenge.crossmint.io/api/polyanets",
            json={"candidateId": "123", "row": 1, "column": 2},
            headers={"Content-Type": "application/json"},
        )

    @patch("app.astral_objects.polyanet.requests.delete")
    def test_delete_http_error(self, mock_delete):
        """
        Test handling of an HTTP error during a DELETE request.

        Simulates a 404 Not Found response from the API when deleting a Polyanet object,
        and verifies that the method raises an HTTPError.
        """
        # Configure the mock to simulate an HTTP error
        mock_delete.return_value = Mock(status_code=404)
        mock_delete.return_value.raise_for_status = Mock(
            side_effect=requests.exceptions.HTTPError("404 Error")
        )

        # Test the delete method
        with self.assertRaises(requests.exceptions.HTTPError):
            self.polyanet.delete((1, 2))


if __name__ == "__main__":
    unittest.main()
