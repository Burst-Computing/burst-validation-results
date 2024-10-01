import json

GRANULARITY = 96
local_counter = 0
remote_counter = 0

with open('outputs.json') as f:
    data = json.load(f)
    for key in data:
        i = 0
        for subkey in data[key]["output_partition_sizes"]:
            if i < GRANULARITY:
                local_counter += data[key]["output_partition_sizes"][subkey]
            else:
                remote_counter += data[key]["output_partition_sizes"][subkey]
            i += 1

print("Local: ", local_counter)
print("Remote: ", remote_counter)

