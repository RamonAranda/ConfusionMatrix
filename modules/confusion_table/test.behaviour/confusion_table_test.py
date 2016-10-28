import unittest
import mock

from confusion_table.src._confusion_table import ConfusionTable


class ConfusionTableTest(unittest.TestCase):

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
            None
        )

    def test_all_properties_match(self):
        self.failUnlessEqual(self.ct.accuracy, 0.5)
        self.failUnlessEqual(self.ct.precision, 0.5)
        self.failUnlessEqual(self.ct.recall, 0.5)
        self.failUnlessEqual(self.ct.specificity, 0.5)
        self.failUnlessEqual(self.ct.f1score, 0.5)
        self.failUnlessEqual(self.ct.fall_out, 0.5)
        self.failUnlessEqual(self.ct.miss_rate, 0.5)
        self.failUnlessEqual(self.ct.FDR, 0.5)
        self.failUnlessEqual(self.ct.NPV, 0.5)
        self.failUnlessEqual(self.ct.PLR, 1)
        self.failUnlessEqual(self.ct.NLR, 1)
        self.failUnlessEqual(self.ct.DOR, 1)

    @mock.patch('confusion_table.src._confusion_table.ConfusionTable.__str__', return_value='potato')
    def test_confusion_table_str(self, mocked_str):
        assert self.ct.__str__() == 'potato'
        print mocked_str.call_count
