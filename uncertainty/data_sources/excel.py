from openpyxl.worksheet import Worksheet
import regex
from openpyxl import load_workbook, workbook


def _base_26_number_plus_1(number: list) -> list:
    number.insert(0, 0)
    index = len(number)
    for n in range(index - 1, -1, -1):
        number[n] += 1
        # keep incrementing elements until we find one that's less than 26
        if number[n] <= 26:
            if number[0] == 0:
                number.pop(0)
            return number
        number[n] = 1


def _convert_str_to_base_26(value: str) -> list:
    # ord("A")==65
    return [ord(c) - 64 for c in value]


def _check_end_after_start(start, end) -> None:
    reverse_start = start[::-1]
    reverse_end = end[::-1]
    e = sum((26 ** i) * ord(c) for i, c in enumerate(reverse_end))
    s = sum((26 ** i) * ord(c) for i, c in enumerate(reverse_start))
    if s > e:
        raise ValueError("start value {0} before end value {1}".format(start, end))


def _check_start_end_acceptable(start: str, end: str) -> None:
    """
    check that the start and end strings for the char getter are acceptable.
    TODO: rename this to something more sensible
    """

    char_regex = regex.compile("[A-Z]+")

    if not char_regex.fullmatch(start) or not char_regex.fullmatch(end):
        raise ValueError("start and end must be characters")

    _check_end_after_start(start, end)


def _get_excel_column_labels(start: str, end: str):
    """
Returns all characters between start, and end in an excel type manner (so Y Z AA AB AC...). Assumes start is before end
    @param start:
    @param end:
    @return list of strings:
    """
    if not start or not end:
        raise ValueError("{0} missing".format("start" if start is None else "end"))

    end = end.upper()
    start = start.upper()

    _check_start_end_acceptable(start, end)

    range_builder = [start]

    start_list = _convert_str_to_base_26(start)
    end_list = _convert_str_to_base_26(end)

    # we always want to add start_list value, we're fairly sure that end >= start
    while start_list != end_list:
        start_list = _base_26_number_plus_1(start_list)
        # convert this funny base 26 list to a string
        range_builder.append("".join([chr(x + 64) for x in start_list]))
    return range_builder


def _get_char_and_num_from_cell_label(label: str) -> tuple:
    cell_regex = regex.compile("([A-Z]+)([0-9]+)")
    m = cell_regex.match(label)
    return m.group(1), int(m.group(2))


def _get_cell_in_range(start, end) -> iter:
    start_char, start_num = _get_char_and_num_from_cell_label(start)
    end_char, end_num = _get_char_and_num_from_cell_label(end)

    if start_num > end_num:
        raise ValueError("{0} needs to come before {1}".format(start_num, end_num))

    chars = _get_excel_column_labels(start_char, end_char)
    nums = range(start_num, end_num + 1)

    return (c + str(n) for c in chars for n in nums)


def _get_data_from_worksheet(worksheet: Worksheet, start_cell: str, end_cell: str) -> tuple:
    # cell_range = _get_cell_in_range(start_cell, end_cell)
    start_char, start_num = _get_char_and_num_from_cell_label(start_cell)
    end_char, end_num = _get_char_and_num_from_cell_label(end_cell)
    values = list()

    for r in range(start_num, end_num + 1):
        row = list()
        for c in _get_excel_column_labels(start_char, end_char):
            row.append(str(worksheet[c + str(r)].value))
        values.append(tuple(row))

    # if we want a row or a column, then flatten it to return a tuple of values,
    # otherwise return a tuple of tuples of valeus
    if start_num == end_num or start_char == end_char:
        return tuple([y for x in values for y in x])
    return tuple(values)


def get_data_from_excel(workbook_name: str, worksheet_name: str, start_cell: str, end_cell: str) -> tuple:
    wb = load_workbook(workbook_name)
    ws = wb.get_sheet_by_name(worksheet_name)
    return _get_data_from_worksheet(ws, start_cell, end_cell)
