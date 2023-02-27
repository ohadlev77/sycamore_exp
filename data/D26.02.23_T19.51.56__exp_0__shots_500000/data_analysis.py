import os
import json
import numpy as np
import matplotlib.pyplot as plt

path = "src/data/D26.02.23_T19.51.56__exp_0__shots_500000"
data_folders = sorted([f"{path}/{dir}" for dir in os.listdir(path) if dir.startswith("circuit")])

all_files = []
for folder in data_folders:
    for file in os.listdir(folder):
        if file.endswith(".json"):
            all_files.append(f"{folder}/{file}")

for index, data_file in enumerate(all_files):
    with open(data_file, "r") as f:
        data = json.load(f)
    
    num_qubits = len(list(data.keys())[0])
    dim = 2 ** num_qubits
    x = [p * dim for p in data.values()]

    plt.hist(x)
    plt.savefig(f"{num_qubits}_{index}_HISTOGRAM.pdf")

