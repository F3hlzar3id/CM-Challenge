from abc import ABC, abstractmethod


class AstralObject(ABC):
    """
    Base class representing a generic astral object.

    It serves a template for astral objects, providing
    abstract methods for posting and deleting objects. It also is
    provides a function to assure the correctness in form for
    the provided data for those methods.
    """

    def __init__(self, candidate_id):
        """
        Initialize an AstralObject instance.

        Args:
            candidate_id (str): The unique identifier for the crossmint's candidate.
        """
        self.name = "AstralObject"
        self.candidate_id = candidate_id

    @abstractmethod
    def post(self, rows_columns_tuple):
        """
        Post the atral object at specified position with given attributes (if given).

        Abstract method to be implemented by subclasses.

        Args:
            rows_columns_tuple (tuple): A tuple, defining the position (row, column) and additional parameters for posting the object.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass

    @abstractmethod
    def delete(self, rows_columns_tuples):
        """
        Delete the object at specified position.

        Abstract method to be implemented by subclasses.

        Args:
            rows_columns_tuple (tuple): A tuple, defining the position (row, column) and additional parameters for posting the object.


        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        pass

    def check_tuples(self, item, len_tuple, in_list=None):
        """
        Validate a tuple for proper length and optional values.

        Args:
            item (tuple): The tuple to validate.
            len_tuple (int): The expected length of the tuple.
            in_list (list, optional): A list of valid values for the last element
                of the tuple. If specified, the last element of the tuple must be in this list.

        Raises:
            AssertionError: If the item is not a tuple, has the wrong length, or
                if its last element is not in the provided list of valid values.
        """
        assert isinstance(item, tuple), "All items must be tuples."
        assert (
            len(item) == len_tuple
        ), f"The tuple {item} should have {len_tuple} elements, but has {len(item)}."
        if in_list:
            assert (
                item[-1] in in_list
            ), f"The last argument of the tuple {item} must be one of {in_list}."
