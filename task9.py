
def duplicate_deletion(input_list: list) -> list:
        dict_keys = []
        dict_values = []
        for dict_el in input_list:
            dict_keys.append(dict_el.keys())
    return output_list


print(duplicate_deletion([{"key1":"value1"}, {'k1':'v1', 'k2':'v2', 'k3':'v3'}, {}, {}, {"key1":"value1"}, {"key1":"value1"}, {"key2":"value2"}]))
