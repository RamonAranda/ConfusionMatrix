import unittest
import mock
from pyrsistent import pmap
from toolz import map

from confusion_matrix.src._confusion_matrix import ConfusionMatrix


class ConfusionMatrixTest(unittest.TestCase):
    def setUp(self):
        self.mocked_object_label_a = mock.MagicMock()
        self.mocked_object_label_b = mock.MagicMock()
        self.confusion_matrix = ConfusionMatrix(
            pmap({
                "a": self.mocked_object_label_a,
                "b": self.mocked_object_label_b
            }),
            None,
            None
        )
        self.attributes = [
            'accuracy', 'precision', 'recall', 'specificity', 'f1score', 'fall_out', 'miss_rate',
            'FDR', 'FOR', 'NPV', 'PLR', 'NLR', 'DOR'
        ]

    def set_attributes(self):
        list(map(
            lambda property_name: setattr(
                type(self.mocked_object_label_a),
                property_name,
                mock.PropertyMock(name=property_name, return_value=1)
            ),
            self.attributes
        ))

    def test_averages(self):
        self.set_attributes()
        list(
            map(
                lambda property_name: self.assertEqual(
                    getattr(self.confusion_matrix, "average_" + property_name),
                    1
                ),
                self.attributes
            )
        )
