from pyrsistent import pmap
from toolz import pipe, curry, partial
from toolz.curried import map, filter
from toolz.dicttoolz import iterkeys, zip, merge

from modules.confusion_matrix.src._confusion_matrix import ConfusionMatrix


def generate_confusion_matrix(confusion_table_generator, formatter, expected, predicted, labels=None):
    prediction_dict = __calculate_prediction_dict(
        expected,
        predicted,
        set(list(expected + predicted)) if labels is None else labels
    )
    confusion_tables = __calculate_confusion_tables(prediction_dict, confusion_table_generator, formatter)
    return ConfusionMatrix(confusion_tables, prediction_dict, formatter)


def __calculate_prediction_dict(expected, predicted, labels):
    return pipe(
        labels,
        __generate_prediction_dict(zip(expected, predicted)),
        pmap
    )


@curry
def __generate_prediction_dict(predictions, labels):
    @curry
    def create_dict_for_label(value, label):
        return pmap({label: value})

    def get_label_predictions(predictions_list, all_labels, label):
        def count_predictions(filtered_predictions_list, target_label):
            return pipe(
                filtered_predictions_list,
                filter(lambda (_, x): x == target_label),
                list,
                len
            )
        filtered_predictions = pipe(
            predictions_list,
            filter(lambda (x, _): x == label)
        )
        count_predictions_partial = \
            partial(count_predictions, list(filtered_predictions))
        return pipe(
            all_labels,
            map(lambda target:
                {target: count_predictions_partial(target)}),
            map(pmap),
            merge,
            pmap
        )
    get_label_predictions_partial = \
        partial(get_label_predictions, list(predictions), labels)
    return pipe(
        labels,
        map(
            lambda label:
            create_dict_for_label(get_label_predictions_partial(label), label)
        ),
        merge,
        pmap
    )


def __calculate_confusion_tables(predictions_dict, confusion_table_generator, formatter):
    def calculate_confusion_table(label):
        return pmap({
            label: confusion_table_generator(predictions_dict, label, formatter)
        })

    return pipe(
        predictions_dict,
        iterkeys,
        map(calculate_confusion_table),
        merge,
        pmap
    )
