import unittest
from app.astral_objects.astral_object import AstralObject


# Dummy subclass to test abstract methods
class DummyAstralObject(AstralObject):
    """
    A dummy subclass of AstralObject used for testing abstract methods.

    Implements the abstract methods `post` and `delete`
    to enable instantiation of the abstract base class.
    """

    def post(self, rows_columns_tuples):
        """Dummy implementation of the abstract `post` method."""
        pass

    def delete(self, rows_columns_tuples):
        """Dummy implementation of the abstract `delete` method."""
        pass


class TestAstralObject(unittest.TestCase):
    """
    Test suite for the AstralObject base class.

    This suite tests the behavior of the `check_tuples` utility method,
    ensuring it validates input tuples correctly.
    """

    def setUp(self):
        """
        Set up a DummyAstralObject instance for testing.
        """
        self.obj = DummyAstralObject("")

    def test_check_tuples_valid_input(self):
        """
        Test `check_tuples` with valid input.

        Verifies that the method does not raise any assertions when given
        a valid tuple, length, and optional value list.
        """
        self.assertIsNone(self.obj.check_tuples((1, 2, "red"), 3, ["red"]))

    def test_check_tuples_invalid_type(self):
        """
        Test `check_tuples` with an invalid type.

        Verifies that the method raises an AssertionError when the input
        is not a tuple.
        """
        with self.assertRaises(AssertionError):
            self.obj.check_tuples("not a tuple", 3)

    def test_check_tuples_invalid_length(self):
        """
        Test `check_tuples` with an invalid tuple length.

        Verifies that the method raises an AssertionError when the tuple
        does not have the expected length.
        """
        with self.assertRaises(AssertionError):
            self.obj.check_tuples((1, 2), 3)

    def test_check_tuples_invalid_value(self):
        """
        Test `check_tuples` with an invalid value in the tuple.

        Verifies that the method raises an AssertionError when the last
        element of the tuple is not in the allowed value list.
        """
        with self.assertRaises(AssertionError):
            self.obj.check_tuples((1, 2, "brown"), 3, ["red"])


if __name__ == "__main__":
    unittest.main()
