import random
import string

# random list from 2 to 10
num_dicts = random.randint(2, 10)

# list for storing generated dictionaries
dict_list = []

# iterate through numbre of dicts to generate random dictionaries
for _ in range(num_dicts):
    num_keys = random.randint(1, 5)
    keys = random.sample(string.ascii_lowercase, num_keys)
    d = {key: random.randint(0, 100) for key in keys}
    dict_list.append(d)

print("Generated list:", dict_list)

# empty dict for final result
result = {}

# dict for tracking keys and their occurrences in dictionaries
key_tracker = {}

# iterate through the list of dictionaries with index starting from 1
for idx, d in enumerate(dict_list, start=1):
    for key, value in d.items():
        if key not in key_tracker:
            key_tracker[key] = []
        key_tracker[key].append((idx, value))

# Iterate through the collected keys
for key, occurrences in key_tracker.items():
    if len(occurrences) == 1:
        idx, value = occurrences[0]
        result[key] = value
    # If the key appears in multiple dictionaries
    else:
        idx, value = max(occurrences, key=lambda x: x[1])
        new_key = f"{key}_{idx}"
        result[new_key] = value

print("Merged dictionary:", result)
