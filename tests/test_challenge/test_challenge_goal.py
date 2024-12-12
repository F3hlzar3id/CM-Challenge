import unittest
import requests
from unittest.mock import patch, Mock
from app.challenge.challenge_goal import ChallengeGoal


class TestChallengeGoal(unittest.TestCase):
    def setUp(self):
        self.challenge = ChallengeGoal()

    @patch("app.challenge.challenge_goal.requests.get")
    def test_get_goal_map_success(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={"goal": [["POLYANET", "SPACE"], ["COMETH", "SOLOON"]]}
            ),
        )
        self.challenge.get_goal_map()

        self.assertEqual(
            self.challenge.get_goal_map(), [["POLYANET", "SPACE"], ["COMETH", "SOLOON"]]
        )

    @patch("app.challenge.challenge_goal.requests.get")
    def test_get_goal_map_http_error(self, mock_get):
        mock_get.return_value = Mock(status_code=404)
        mock_get.return_value.raise_for_status = Mock(
            side_effect=requests.exceptions.HTTPError("404 Error")
        )

        with self.assertRaises(requests.exceptions.HTTPError):
            self.challenge.get_goal_map()

    @patch("app.challenge.challenge_goal.ClassIdentifier")
    @patch("app.challenge.challenge_goal.requests.get")
    def test_solve_challengue_1(self, mock_get, mock_class_identifier):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={"goal": [["POLYANET", "SPACE"], ["COMETH", "SOLOON"]]}
            ),
        )
        self.challenge.get_goal_map()

        mock_class_instance = mock_class_identifier.return_value
        mock_class_instance.get_class_info.return_value = {
            "polyanet": Mock(),
            "soloon": Mock(),
            "cometh": Mock(),
        }
        mock_class_instance.create_instance.side_effect = (
            lambda class_name, candidate_id: Mock(post=Mock())
        )

        self.challenge.solve_challengue_1()

        mock_class_instance.create_instance.assert_any_call(
            "polyanet", candidate_id=self.challenge.candidate_id
        )
        mock_class_instance.create_instance.assert_any_call(
            "soloon", candidate_id=self.challenge.candidate_id
        )
        mock_class_instance.create_instance.assert_any_call(
            "cometh", candidate_id=self.challenge.candidate_id
        )

    @patch("app.challenge.challenge_goal.ClassIdentifier")
    @patch("app.challenge.challenge_goal.requests.get")
    def test_solve_challengue_1_with_retries(self, mock_get, mock_class_identifier):
        # Mock the goal map API response
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={"goal": [["POLYANET", "SPACE"], ["COMETH", "SOLOON"]]}
            ),
        )
        self.challenge.get_goal_map()
        polyanet_instance = Mock()
        soloon_instance = Mock()
        cometh_instance = Mock()

        # Simulate retries for polyanet
        polyanet_instance.post.side_effect = [
            requests.exceptions.HTTPError(response=Mock(status_code=429)),
            requests.exceptions.HTTPError(response=Mock(status_code=429)),
            None,  # Success on third attempt
        ]
        soloon_instance.post = Mock()
        cometh_instance.post = Mock()

        mock_class_instance = mock_class_identifier.return_value
        mock_class_instance.get_class_info.return_value = {
            "polyanet": Mock(),
            "soloon": Mock(),
            "cometh": Mock(),
        }
        mock_class_instance.create_instance.side_effect = (
            lambda class_name, candidate_id: {
                "polyanet": polyanet_instance,
                "soloon": soloon_instance,
                "cometh": cometh_instance,
            }[class_name]
        )

        # Run the solve_challengue_1 method
        self.challenge.solve_challengue_1()
        # Verify retries for polyanet
        self.assertEqual(polyanet_instance.post.call_count, 3)  # 2 retries + 1 success

        # Ensure other items are posted correctly
        soloon_instance.post.assert_called_once_with((1, 1))
        cometh_instance.post.assert_called_once_with((1, 0))

    @patch("app.challenge.challenge_goal.ClassIdentifier")
    @patch("app.challenge.challenge_goal.requests.get")
    def test_solve_challengue_1_max_retries_exceeded(
        self, mock_get, mock_class_identifier
    ):
        # Mock ClassIdentifier and instances
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={"goal": [["POLYANET", "SPACE"], ["COMETH", "SOLOON"]]}
            ),
        )
        self.challenge.get_goal_map()
        polyanet_instance = Mock()
        polyanet_instance.post.side_effect = [
            requests.exceptions.HTTPError(response=Mock(status_code=429))
            for _ in range(5)
        ]  # Always fails

        # Mock ClassIdentifier behavior
        mock_class_instance = mock_class_identifier.return_value
        mock_class_instance.get_class_info.return_value = {"polyanet": Mock()}
        mock_class_instance.create_instance.side_effect = (
            lambda name, candidate_id: polyanet_instance
        )

        # Run solve_challengue_2 and expect an exception
        with self.assertRaises(Exception) as context:
            self.challenge.solve_challengue_2()
        self.assertIn("Max retries exceeded", str(context.exception))

    @patch("app.challenge.challenge_goal.ClassIdentifier")
    @patch("app.challenge.challenge_goal.requests.get")
    def test_solve_challengue_2_success(self, mock_get, mock_class_identifier):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "goal": [["POLYANET", "SPACE"], ["UP_COMETH", "PURPLE_SOLOON"]]
                }
            ),
        )
        self.challenge.get_goal_map()
        # Mock ClassIdentifier and instances
        polyanet_instance = Mock()
        cometh_instance = Mock()
        soloon_instance = Mock()

        # Configure post methods to succeed
        polyanet_instance.post = Mock()
        cometh_instance.post = Mock()
        soloon_instance.post = Mock()

        # Mock ClassIdentifier behavior
        mock_class_instance = mock_class_identifier.return_value
        mock_class_instance.get_class_info.return_value = {
            "polyanet": Mock(),
            "cometh": Mock(),
            "soloon": Mock(),
        }
        mock_class_instance.create_instance.side_effect = lambda name, candidate_id: {
            "polyanet": polyanet_instance,
            "cometh": cometh_instance,
            "soloon": soloon_instance,
        }[name]

        # Run solve_challengue_2
        self.challenge.solve_challengue_2()

        # Verify calls to post
        polyanet_instance.post.assert_called_once_with((0, 0))
        cometh_instance.post.assert_called_once_with((1, 0, "up"))
        soloon_instance.post.assert_called_once_with((1, 1, "purple"))

    @patch("app.challenge.challenge_goal.ClassIdentifier")
    @patch("app.challenge.challenge_goal.requests.get")
    def test_solve_challengue_2_with_retries(self, mock_get, mock_class_identifier):
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "goal": [["POLYANET", "SPACE"], ["UP_COMETH", "PURPLE_SOLOON"]]
                }
            ),
        )
        self.challenge.get_goal_map()
        # Mock ClassIdentifier and instances
        polyanet_instance = Mock()
        polyanet_instance.post.side_effect = [
            requests.exceptions.HTTPError(response=Mock(status_code=429)),
            requests.exceptions.HTTPError(response=Mock(status_code=429)),
            None,  # Succeeds on third attempt
        ]
        cometh_instance = Mock()
        soloon_instance = Mock()

        # Mock ClassIdentifier behavior
        mock_class_instance = mock_class_identifier.return_value
        mock_class_instance.get_class_info.return_value = {
            "polyanet": Mock(),
            "cometh": Mock(),
            "soloon": Mock(),
        }
        mock_class_instance.create_instance.side_effect = lambda name, candidate_id: {
            "polyanet": polyanet_instance,
            "cometh": cometh_instance,
            "soloon": soloon_instance,
        }[name]

        # Run solve_challengue_2
        self.challenge.solve_challengue_2()

        # Verify retries for polyanet
        self.assertEqual(polyanet_instance.post.call_count, 3)  # 2 retries + 1 success

    @patch("app.challenge.challenge_goal.ClassIdentifier")
    @patch("app.challenge.challenge_goal.requests.get")
    def test_solve_challengue_2_max_retries_exceeded(
        self, mock_get, mock_class_identifier
    ):
        # Mock ClassIdentifier and instances
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(
                return_value={
                    "goal": [["POLYANET", "SPACE"], ["UP_COMETH", "PURPLE_SOLOON"]]
                }
            ),
        )
        self.challenge.get_goal_map()
        polyanet_instance = Mock()
        polyanet_instance.post.side_effect = [
            requests.exceptions.HTTPError(response=Mock(status_code=429))
            for _ in range(5)
        ]  # Always fails

        # Mock ClassIdentifier behavior
        mock_class_instance = mock_class_identifier.return_value
        mock_class_instance.get_class_info.return_value = {"polyanet": Mock()}
        mock_class_instance.create_instance.side_effect = (
            lambda name, candidate_id: polyanet_instance
        )

        # Run solve_challengue_2 and expect an exception
        with self.assertRaises(Exception) as context:
            self.challenge.solve_challengue_2()
        self.assertIn("Max retries exceeded", str(context.exception))


if __name__ == "__main__":
    unittest.main()
