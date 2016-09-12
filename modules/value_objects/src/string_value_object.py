from modules.value_objects.src.value_object import ValueObject


class StringValueObject(ValueObject):
    def __init__(self, value):
        super(StringValueObject, self).__init__(value)

    def __str__(self):
        return self.get_value().__str__()

    def __repr__(self):
        return "StringValueObject({})".format(self.get_value())

    def __add__(self, other):
        return StringValueObject(self.get_value() + other.__str__())

    def __mul__(self, other):
        return StringValueObject(self.get_value() * other)

    def __contains__(self, item):
        return item in self.get_value()

    def __len__(self):
        return len(self.get_value())
