import unittest
from modules.value_objects.src.value_object import ValueObject


class ValueObjectTest(unittest.TestCase):
    class ValueObjectMock(ValueObject):
        pass

    def setUp(self):
        self.value = 1
        self.value_object_1 = self.ValueObjectMock(self.value)
        self.value_object_2 = self.ValueObjectMock(self.value)

    def test_instances_has_same_value(self):
        self.failUnlessEqual(self.value_object_1.get_value(), self.value)
        self.failUnlessEqual(self.value_object_2.get_value(), self.value)

    def test_instances_are_equal(self):
        self.assertTrue(self.value_object_1 == self.value_object_2)

    def test_instances_are_not_the_same_instance(self):
        self.assertTrue(self.value_object_1 is not self.value_object_2)
