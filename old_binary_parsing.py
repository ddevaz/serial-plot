def dump_to_csv(filename, lst):
    resultFile = open(filename,'w', newline='')
    wr = csv.writer(resultFile, dialect='excel')
    for x in lst:
        wr.writerow([x])


def hex_to_uint16(str):
    rev_string = swap_bytes_uint16(str)
    return int(rev_string, 16)


def swap_bytes_uint16(str):
    firstbyte, secondbyte = str[:2], str[2:]
    return secondbyte + firstbyte

# Parses out binary data based on custom delimiter
def parse_blob(str, **kwargs):
    delimiter = kwargs.get('delimiter')
    max_val = kwargs.get('max_val')
    if delimiter is None or max_val is None:
        raise ValueError('Need to specify delimiter and max_val')
    seperated_list = str.split(delimiter)
    clean_list = [x for x in seperated_list if x]
    data = [hex_to_uint16(x) for x in clean_list]
    cleaned_data = [x for x in data if x < max_val]
    return cleaned_data