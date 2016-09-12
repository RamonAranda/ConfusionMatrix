import unittest
from modules.value_objects.src.string_value_object import StringValueObject


class StringValueObjectTest(unittest.TestCase):

    def setUp(self):
        self.basestring = "test me please!"
        self.string = StringValueObject("test me please!")

    def test_instance_repr(self):
        self.failUnlessEqual(
            self.string.__repr__(),
            "StringValueObject({})".format(self.basestring),
        )

    def test_instance_str(self):
        self.failUnlessEqual(self.string.__str__(), self.basestring.__str__())

    def test_instance_is_not_mutable(self):
        self.assertFalse(
            self.string + StringValueObject("a") == self.string
        )

    def test_contains(self):
        self.failUnless("test" in self.string)
