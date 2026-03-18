import random
import string
from typing import Dict, List, Tuple


def generate_random_dictionary() -> Dict[str, int]:
    # Generate one random dictionary with unique lowercase letter keys.
    num_keys = random.randint(1, 5)
    keys = random.sample(string.ascii_lowercase, num_keys)
    return {key: random.randint(0, 100) for key in keys}


def generate_dictionary_list() -> List[Dict[str, int]]:
    # Generate a random list of dictionaries.
    num_dicts = random.randint(2, 10)
    return [generate_random_dictionary() for _ in range(num_dicts)]


def collect_key_occurrences(
    dict_list: List[Dict[str, int]],
) -> Dict[str, List[Tuple[int, int]]]:
    key_occurrences: Dict[str, List[Tuple[int, int]]] = {}

    for index, current_dict in enumerate(dict_list, start=1):
        for key, value in current_dict.items():
            key_occurrences.setdefault(key, []).append((index, value))

    return key_occurrences


def build_result_dictionary(
    key_occurrences: Dict[str, List[Tuple[int, int]]],
) -> Dict[str, int]:
    result: Dict[str, int] = {}

    for key, occurrences in key_occurrences.items():
        if len(occurrences) == 1:
            _, value = occurrences[0]
            result[key] = value
        else:
            index, value = max(occurrences, key=lambda item: item[1])
            result[f"{key}_{index}"] = value

    return result


def merge_dictionaries_functionally(dict_list: List[Dict[str, int]]) -> Dict[str, int]:
    key_occurrences = collect_key_occurrences(dict_list)
    return build_result_dictionary(key_occurrences)


def main() -> None:
    dict_list = generate_dictionary_list()
    result = merge_dictionaries_functionally(dict_list)

    print("Generated dictionaries:")
    for item in dict_list:
        print(item)

    print("\nResult:")
    print(result)


if __name__ == "__main__":
    main()
