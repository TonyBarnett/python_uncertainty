import regex


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


def _get_cell_in_range(start, end) -> iter:
    cell_regex = regex.compile("([A-Z]+)([0-9]+)")
    start_match = cell_regex.match(start)
    end_match = cell_regex.match(end)
    start_char = start_match.group(1)
    start_num = int(start_match.group(2))
    end_char = end_match.group(1)
    end_num = int(end_match.group(2))

    chars = _get_excel_column_labels(start_char, end_char)
    nums = range(start_num, end_num + 1)

    return (c + str(n) for c in chars for n in nums)


def _get_data_from_workbook(workbook, worksheet_name: str, start_cell: str, end_cell: str) -> tuple:
    ws = workbook.get_sheet_by_name(worksheet_name)
    cell_range = _get_cell_in_range(start_cell, end_cell)
    values = list()
    for cell in cell_range:
        values.append(str(ws[cell].value))
    return tuple(values)

