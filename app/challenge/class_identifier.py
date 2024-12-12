from app.astral_objects.astral_object import AstralObject


class ClassIdentifier:
    """
    A utility class to dynamically identify subclasses of AstralObject and manage their instances.

    This class is responsible for discovering all subclasses of `AstralObject` at runtime,
    storing them in a dictionary, and providing mechanisms to retrieve information
    about them or create instances dynamically.
    """

    def __init__(self):
        """
        Initializes the ClassIdentifier instance.

        Discovers all subclasses of `AstralObject` and stores them in a dictionary
        with their lowercase names as keys.
        """
        self.class_dict = self._identify_classes()

    def _identify_classes(self):
        """
        Identify all subclasses of AstralObject.

        Find all direct subclasses of `AstralObject` and maps their lowercase class names to their class objects.

        Returns:
            dict: A dictionary where keys are lowercase class names (str) and values
                are the corresponding class objects for later use.
        """
        class_dict = {}
        for subclass in AstralObject.__subclasses__():
            # print(f"Found subclass: {subclass.__name__}")
            class_dict[subclass.__name__.lower()] = subclass
        return class_dict

    def get_class_info(self):
        """
        Retrieve information about the identified classes.

        Returns:
            dict: The dictionary of identified subclasses, where keys are lowercase
                class names and values are the corresponding class objects.
        """

        return self.class_dict

    def create_instance(self, class_name, *args, **kwargs):
        """
        Create an instance of the identified class.

        Args:
            class_name (str): The name of the class (case-insensitive) to instantiate.
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            object: An instance of the specified class.

        Raises:
            ValueError: If no class matching the given name is found in the dictionary.
        """
        class_type = self.class_dict.get(class_name.lower())
        if class_type:
            return class_type(*args, **kwargs)
        else:
            raise ValueError(f"No class found for name {class_name}")
