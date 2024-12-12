import unittest
from unittest.mock import patch, MagicMock
from app.challenge.class_identifier import ClassIdentifier
from app.astral_objects.astral_object import AstralObject
from app.astral_objects.polyanet import Polyanet
from app.astral_objects.soloon import Soloon
from app.astral_objects.cometh import Cometh


class TestClassIdentifier(unittest.TestCase):
    def setUp(self):
        self.identifier = ClassIdentifier()

    def test_identify_classes(self):
        class_info = self.identifier.get_class_info()
        self.assertIn("polyanet", class_info)
        self.assertIn("soloon", class_info)
        self.assertIn("cometh", class_info)
        self.assertNotIn("astralobject", class_info)

    def test_create_instance(self):
        instance = self.identifier.create_instance("polyanet", candidate_id="123")
        self.assertIsInstance(instance, Polyanet)

    def test_create_instance_invalid_class(self):
        # Test behavior for invalid class name
        with self.assertRaises(ValueError) as context:
            self.identifier.create_instance("unknown_class")
        self.assertEqual(
            str(context.exception), "No class found for name unknown_class"
        )


if __name__ == "__main__":
    unittest.main()
