from pyrsistent import pvector
from toolz import pipe
from toolz.curried import reduce, map
from toolz.dicttoolz import iterkeys, itervalues
from modules.value_objects.src.string_value_object import StringValueObject

__WHITESPACE = StringValueObject(" ")
__VERTICAL_SEPARATOR = StringValueObject("|")
__LINE_BREAK = StringValueObject("\n")
__HORIZONTAL_SEPARATOR = StringValueObject("-")


def __first(sequence):
    for _ in sequence:
        return _


def format_dict_as_grid(data):
    max_length_per_column = __calculate_max_str_length_per_column(data)
    separator = __get_row_separator(max_length_per_column)
    headers = __get_header(
        pipe(data, itervalues, __first, iterkeys), max_length_per_column
    )
    rows = __get_rows(data, max_length_per_column)
    return StringValueObject(separator + headers + separator + rows)


def __calculate_max_str_length_per_column(data):
    def __calculate_max_column_length(column_key):
        max_value_length = pipe(
            data,
            iterkeys,
            map(lambda key: data[key][column_key]),
            pvector,
            map(str),
            map(len),
            max
        )
        return max(max_value_length, len(str(column_key)))
    max_values_column_length = pipe(
        data,
        itervalues,
        __first,
        iterkeys,
        map(__calculate_max_column_length),
        pvector
    )
    max_key_length = pipe(
        data, iterkeys, map(str), map(len), pvector, max, lambda x: [x], pvector
    )
    return max_key_length + max_values_column_length


def __get_row_separator(max_length_per_column):
    n_whitespaces = 2 * len(__WHITESPACE) * len(max_length_per_column)
    n_vertial_separators = \
        len(__VERTICAL_SEPARATOR) * len(max_length_per_column) + 1
    length_of_all_col_names = sum(max_length_per_column)
    return StringValueObject(
        __HORIZONTAL_SEPARATOR *
        ((n_whitespaces + n_vertial_separators + length_of_all_col_names) /
         len(__HORIZONTAL_SEPARATOR))
    ) + __LINE_BREAK


def __get_header(headers_list, max_length_per_column):
    def get_empty_header(max_length):
        return StringValueObject(
            __VERTICAL_SEPARATOR +
            __WHITESPACE * (max_length + 2)
        )

    def get_column_header(header_name, max_col_length):
        return StringValueObject(
            __VERTICAL_SEPARATOR + __WHITESPACE + header_name +
            (__WHITESPACE * (max_col_length - len(str(header_name)) + 1))
        )

    empty_header = get_empty_header(max_length_per_column[0])
    headers = pipe(
        zip(headers_list, max_length_per_column[1:]),
        map(lambda (header_name, length):
            get_column_header(header_name, length)),
        list,
        reduce(lambda x, y: x + y)
    )
    return empty_header + headers + __VERTICAL_SEPARATOR + __LINE_BREAK


def __get_rows(data, max_length_per_column):
    return pipe(
        data,
        iterkeys,
        map(lambda key: __get_row(data, key, max_length_per_column)),
        reduce(lambda x, y: x + y)
    )


def __get_row(data, class_key, max_length_per_column):
    def format_value(value, max_len):
        return __VERTICAL_SEPARATOR + __WHITESPACE + str(value) + \
               __WHITESPACE * ((max_len - len(str(value))) + 1)

    row_header = __VERTICAL_SEPARATOR + __WHITESPACE + \
                 str(class_key) + \
                 __WHITESPACE * \
                 (max_length_per_column[0] - len(str(class_key)) + 1)
    row_values = pipe(
        zip(data[class_key].itervalues(), max_length_per_column[1:]),
        map(lambda (value, max_len): format_value(value, max_len)),
        list,
        reduce(lambda x, y: x + y),
    )
    return row_header + row_values + __VERTICAL_SEPARATOR + \
           __LINE_BREAK + __get_row_separator(max_length_per_column)
