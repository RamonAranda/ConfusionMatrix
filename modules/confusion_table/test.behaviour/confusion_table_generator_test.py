import unittest

from mock import mock
from pyrsistent import pmap

from confusion_table.src._confusion_table import ConfusionTable
from confusion_table.src._confusion_table_generator import generate_confusion_table


class ConfusionTableGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.format = mock.MagicMock(return_value=lambda x: str(x))
        self.label_1 = "a"
        self.label_2 = "b"
        self.true_positive = 8
        self.true_negative = 8
        self.false_positive = 8
        self.false_negative = 8
        self.confusion_table = ConfusionTable(
            self.label_1,
            self.true_positive,
            self.true_negative,
            self.false_positive,
            self.false_negative,
            self.format
        )
        self.predictions = pmap({
            self.label_1: pmap({
                self.label_1: self.true_positive,
                self.label_2: self.false_positive,
            }),
            self.label_2: pmap({
                self.label_1: self.false_negative,
                self.label_2: self.true_negative
            })
        })

    def test_generated_confusion_table(self):
        generated_confusion_table_string = generate_confusion_table(
            self.predictions,
            self.label_1,
            self.format
        ).__str__()

        self.assertEqual(self.format.call_count, 1)

        self.assertEqual(
            generated_confusion_table_string,
            self.confusion_table.__str__()
        )

        self.assertEqual(self.format.call_count, 2)
