from pyrsistent import pmap


class ConfusionTable(object):

    def __init__(self, class_name, true_positive, true_negative, false_positive,
                 false_negative, format_fn):
        self.__class_name = class_name
        self.__true_positive = true_positive
        self.__true_negative = true_negative
        self.__false_positive = false_positive
        self.__false_negative = false_negative
        self.__format_function = format_fn

    def __divide_zeroing_division_by_zero(self, x, y):
        try:
            result = x / float(y)
        except ZeroDivisionError:
            result = .0
        return result

    @property
    def accuracy(self):
        """
            Accuracy (ACC): (True Pos + True Neg) / Population
        """
        return self.__divide_zeroing_division_by_zero(
            self.__true_positive + self.__true_negative,
            self.__true_positive + self.__true_negative +
            self.__false_negative + self.__false_positive
        )

    @property
    def precision(self):
        """
            Positive Predictive Value (Precision or PPV):
                True Positive / Outcome Positive
        """
        return self.__divide_zeroing_division_by_zero(
            self.__true_positive, self.__true_positive + self.__false_positive
        )

    @property
    def recall(self):
        """
            True Positive Rate (Sensitivity or Recall or TPR):
                True Positive / Condition Positive
        """
        return self.__divide_zeroing_division_by_zero(
            self.__true_positive, self.__true_positive + self.__false_negative
        )

    @property
    def specificity(self):
        """
            True Negative Rate (Specificity or TNR):
                True Negative / Condition Negative
        """
        return self.__divide_zeroing_division_by_zero(
            self.__true_negative, self.__true_negative + self.__false_positive
        )

    @property
    def f1score(self):
        """
            F-Score or F-Measure (Measure of a test's accuracy):
                2 * (recall * precision) / (recall + precision)
        """
        return 2 * self.__divide_zeroing_division_by_zero(
            self.recall * self.precision, self.recall + self.precision
        )

    @property
    def fall_out(self):
        """
            False Positive Rate (Fall-out or FPR):
                False Positive / Condition Negative
        """
        return self.__divide_zeroing_division_by_zero(
            self.__false_positive, self.__false_positive + self.__true_negative
        )

    @property
    def miss_rate(self):
        """
            False Negative Rate (Miss Rate or FNR):
                False Negative / Condition Positive
        """
        return self.__divide_zeroing_division_by_zero(
            self.__false_negative, self.__false_negative + self.__true_positive
        )

    @property
    def FDR(self):
        """
            False Discovery Rate: False Positive / Outcome Positive
        """
        return self.__divide_zeroing_division_by_zero(
            self.__false_positive, self.__true_positive + self.__false_positive
        )

    @property
    def FOR(self):
        """
            False Omission Rate (FOR): False Negative / Outcome Negative
        """
        return self.__divide_zeroing_division_by_zero(
            self.__false_negative, self.__false_negative + self.__true_negative
        )

    @property
    def NPV(self):
        """
            Negative Predictive Value (NPV): True Negative / Outcome Negative
        """
        return self.__divide_zeroing_division_by_zero(
            self.__true_negative, self.__false_negative + self.__true_negative
        )

    @property
    def PLR(self):
        """
            Positive Likelihood Ratio (LR+ or PLR):
                True Positive Rate / False Positive Rate
        """
        return self.__divide_zeroing_division_by_zero(
            self.recall, self.fall_out
        )

    @property
    def NLR(self):
        """
            Negative Likelihood Ratio (LR- or NLR):
                False Negative Rate / True Positive Rate
        """
        return self.__divide_zeroing_division_by_zero(
            self.miss_rate, self.specificity
        )

    @property
    def DOR(self):
        """
            Diagnostic Odds Ratio (DOR): LR+ / LR-
        """
        return self.__divide_zeroing_division_by_zero(self.PLR, self.NLR)

    def __str__(self):
        """
            Returns ConfusionTable instance as a Grid
        """
        table_values = pmap({
            "true_positive": pmap({str(self.__class_name): self.__true_positive}),
            "true_negative": pmap({str(self.__class_name): self.__true_negative}),
            "false_positive": pmap({str(self.__class_name): self.__false_positive}),
            "false_negative": pmap({str(self.__class_name): self.__false_negative})
        })
        return self.__format_function(table_values).__str__()

    def get_class_name(self):
        return self.__class_name
