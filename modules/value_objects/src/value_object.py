from abc import ABCMeta


class ValueObject(object):
    __metaclass__ = ABCMeta

    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def __eq__(self, other):
        return self.get_value() == other.get_value() \
               and isinstance(other, self.__class__)

    def __repr__(self):
        return "ValueObject({})".format(self.get_value())
