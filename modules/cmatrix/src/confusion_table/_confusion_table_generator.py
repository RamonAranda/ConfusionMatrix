from modules.cmatrix.src.confusion_table._confusion_table import ConfusionTable


def generate_confusion_table(predicted_values, label, formatter):
    true_positive = predicted_values[label][label]
    false_positive = sum(
        predicted_values[label][iter_labels]
        for iter_labels in predicted_values.keys()
    ) - true_positive
    false_negative = sum(
        predicted_values[iter_labels][label]
        for iter_labels in predicted_values.keys()
    ) - true_positive
    true_negative = sum(
        value
        for iter_labels in predicted_values.values()
        for value in iter_labels.values()
    ) - true_positive - false_negative - false_positive
    return ConfusionTable(
        label,
        true_positive,
        true_negative,
        false_positive,
        false_negative,
        formatter
    )
