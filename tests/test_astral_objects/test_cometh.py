import unittest

from unittest.mock import patch, Mock
import requests
from app.astral_objects.cometh import Cometh


class TestCometh(unittest.TestCase):
    """
    Test suite for the Cometh class.

    This test suite verifies the behavior of the Cometh class, including:
    - Successful posting and deletion of Cometh objects.
    - Handling HTTP errors during API interactions.
    """

    def setUp(self):
        """
        Set up a Cometh instance with a mock candidate ID for testing.
        """
        self.cometh = Cometh(candidate_id="123")

    @patch("app.astral_objects.cometh.requests.post")
    def test_post_success(self, mock_post):
        """
        Test successful posting of a Cometh object.

        Simulates a 200 OK response from the API when posting a Cometh object,
        and verifies that the correct parameters are sent in the API request.
        """
        mock_post.return_value = Mock(status_code=200)
        mock_post.return_value.raise_for_status = Mock()

        self.cometh.post((1, 2, "up"))
        mock_post.assert_called_once_with(
            "https://challenge.crossmint.io/api/comeths",
            json={"candidateId": "123", "row": 1, "column": 2, "direction": "up"},
            headers={"Content-Type": "application/json"},
        )

    @patch("app.astral_objects.cometh.requests.post")
    def test_post_http_error(self, mock_post):
        """
        Test handling of an HTTP error during a POST request.

        Simulates a 404 Not Found response from the API when posting a Cometh object,
        and verifies that the method raises an HTTPError.
        """

        mock_post.return_value = Mock(status_code=404)
        mock_post.return_value.raise_for_status = Mock(
            side_effect=requests.exceptions.HTTPError("404 Error")
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            self.cometh.post((1, 2, "up"))

    @patch("app.astral_objects.cometh.requests.delete")
    def test_delete_success(self, mock_delete):
        """
        Test successful deletion of a Cometh object.

        Simulates a 200 OK response from the API when deleting a Cometh object,
        and verifies that the correct parameters are sent in the API request.
        """
        mock_delete.return_value = Mock(status_code=200)
        mock_delete.return_value.raise_for_status = Mock()

        self.cometh.delete((1, 2))
        mock_delete.assert_called_once_with(
            "https://challenge.crossmint.io/api/comeths",
            json={"candidateId": "123", "row": 1, "column": 2},
            headers={"Content-Type": "application/json"},
        )

    @patch("app.astral_objects.cometh.requests.delete")
    def test_delete_http_error(self, mock_delete):
        """
        Test handling of an HTTP error during a DELETE request.

        Simulates a 404 Not Found response from the API when deleting a Cometh object,
        and verifies that the method raises an HTTPError.
        """
        mock_delete.return_value = Mock(status_code=404)
        mock_delete.return_value.raise_for_status = Mock(
            side_effect=requests.exceptions.HTTPError("404 Error")
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            self.cometh.delete((1, 2))


if __name__ == "__main__":
    unittest.main()
