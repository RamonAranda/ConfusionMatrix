import unittest
from pyrsistent import pmap
from modules.cmatrix.src.confusion_matrix._confusion_matrix_generator import generate_confusion_matrix
from modules.cmatrix.src.confusion_table._confusion_table import ConfusionTable
from modules.cmatrix.src.confusion_table._confusion_table_generator import generate_confusion_table
from modules.formatter.src._formatter import format_dict_as_grid


class IntegrationTest(unittest.TestCase):

    def setUp(self):
        self.label_1 = "a"
        self.label_2 = "b"
        self.label_3 = "c"
        self.true_positive = 8
        self.true_negative = 8
        self.false_positive = 8
        self.false_negative = 8
        self.ct = ConfusionTable(
            self.label_1,
            self.true_positive,
            self.true_negative,
            self.false_positive,
            self.false_negative,
            format_dict_as_grid
        )

    def test_generator_returns_confusion_table_correctly_with_two_classes(self):
        predictions = pmap({
            self.label_1: pmap({
                self.label_1: self.true_positive,
                self.label_2: self.false_positive,
            }),
            self.label_2: pmap({
                self.label_1: self.false_negative,
                self.label_2: self.true_negative
            })
        })
        confusion_table = generate_confusion_table(predictions, self.label_1, format_dict_as_grid)
        self.failUnlessEqual(self.ct.__str__(), confusion_table.__str__())

    def test_generator_returns_confusion_table_correctly_with_three_classes(self):
        predictions = pmap({
            self.label_1: pmap({
                self.label_1: self.true_positive,
                self.label_2: self.false_positive / 2,
                self.label_3: self.false_positive / 2
            }),
            self.label_2: pmap({
                self.label_1: self.false_negative / 2,
                self.label_2: self.true_negative / 2,
                self.label_3: 0
            }),
            self.label_3: pmap({
                self.label_1: self.false_negative / 2,
                self.label_2: 0,
                self.label_3: self.true_negative / 2
            })
        })
        confusion_table = generate_confusion_table(predictions, self.label_1, format_dict_as_grid)
        self.failUnlessEqual(self.ct.__str__(), confusion_table.__str__())
