import numpy as np
from pyrsistent import pmap
from toolz import pipe
from toolz.curried import map, reduce
from toolz.dicttoolz import itervalues


class ConfusionMatrix(object):
    def __init__(self, confusion_tables,
                 predictions_dict, format_fn):
        self.__confusion_tables = pmap(confusion_tables)
        self.__predictions_dict = pmap(predictions_dict)
        self.__format_function = format_fn

    def __calculate_average(self, fn):
        return np.mean(list(map(fn, self.__confusion_tables.values())))

    @property
    def average_accuracy(self):
        return self.__calculate_average(lambda table: table.accuracy)

    @property
    def average_precision(self):
        return self.__calculate_average(lambda table: table.precision)

    @property
    def average_recall(self):
        return self.__calculate_average(lambda table: table.recall)

    @property
    def average_specificity(self):
        return self.__calculate_average(lambda table: table.specificity)

    @property
    def average_f1score(self):
        return self.__calculate_average(lambda table: table.f1score)

    @property
    def average_fall_out(self):
        return self.__calculate_average(lambda table: table.fall_out)

    @property
    def average_miss_rate(self):
        return self.__calculate_average(lambda table: table.miss_rate)

    @property
    def average_FDR(self):
        return self.__calculate_average(lambda table: table.FDR)

    @property
    def average_FOR(self):
        return self.__calculate_average(lambda table: table.FOR)

    @property
    def average_NPV(self):
        return self.__calculate_average(lambda table: table.NPV)

    @property
    def average_PLR(self):
        return self.__calculate_average(lambda table: table.PLR)

    @property
    def average_NLR(self):
        return self.__calculate_average(lambda table: table.NLR)

    @property
    def average_DOR(self):
        return self.__calculate_average(lambda table: table.DOR)

    def __str__(self):
        return self.__format_function(self.__predictions_dict).__str__()

    def log_metrics(self, log_level='basic'):
        avg_metrics_dict = pmap({
            "basic": self.__get_basic_average_metrics,
            "all": self.__get_all_average_metrics
        })[log_level]()
        metrics_dict = pmap({
            "basic": self.__get_basic_metrics_for_each_class,
            "all": self.__get_all_metrics_for_each_class
        })[log_level]()
        return self.__format_function(avg_metrics_dict), self.__format_function(metrics_dict)

    def __get_basic_average_metrics(self):
        return pmap({
            "average": pmap({
                "accuracy": self.average_accuracy,
                "precision": self.average_precision,
                "recall": self.average_recall,
                "specificity": self.average_specificity,
                "f1score": self.average_f1score
            })
        })

    def __get_all_average_metrics(self):
        return pmap({
            "average": pmap({
                "Accuracy": self.average_accuracy,
                "Precision": self.average_precision,
                "Recall": self.average_recall,
                "Specificity": self.average_specificity,
                "F1score": self.average_f1score,
                "Fall Out": self.average_fall_out,
                "Miss Rate": self.average_miss_rate,
                "False Discovery Rate": self.average_FDR,
                "False Omission Rate": self.average_FOR,
                "Negative Predictive Value": self.average_NPV,
                "Positive Likelihood Ratio": self.average_PLR,
                "Negative Likelihood Ratio": self.average_NLR,
                "Diagnostic Odds Ratio": self.average_DOR,
            })
        })

    def __get_basic_metrics_for_each_class(self):
        def __get_basic_metrics_for_class(confusion_table):
            return pmap({
                str(confusion_table.get_class_name()): pmap({
                    "Accuracy": confusion_table.accuracy,
                    "Precision": confusion_table.precision,
                    "Recall": confusion_table.recall,
                    "Specificity": confusion_table.specificity,
                    "F1score": confusion_table.f1score
                })
            })
        return pipe(
            self.__confusion_tables,
            itervalues,
            map(__get_basic_metrics_for_class),
            reduce(lambda x, y: x + y),
        )

    def __get_all_metrics_for_each_class(self):
        def __get_all_metrics_for_class(confusion_table):
            return pmap({
                str(confusion_table.get_class_name()): pmap({
                    "Accuracy": confusion_table.accuracy,
                    "Precision": confusion_table.precision,
                    "Recall": confusion_table.recall,
                    "Specificity": confusion_table.specificity,
                    "F1score": confusion_table.f1score,
                    "Fall Out": confusion_table.fall_out,
                    "Miss Rate": confusion_table.miss_rate,
                    "False Discovery Rate": confusion_table.FDR,
                    "False Omission Rate": confusion_table.FOR,
                    "Negative Predictive Value": confusion_table.NPV,
                    "Positive Likelihood Ratio": confusion_table.PLR,
                    "Negative Likelihood Ratio": confusion_table.NLR,
                    "Diagnostic Odds Ratio": confusion_table.DOR,
                })
            })
        return pipe(
            self.__confusion_tables,
            itervalues,
            map(__get_all_metrics_for_class),
            reduce(lambda x, y: x + y),
        )
