import pandas as pd

data = pd.read_csv(
    "/home/ohad/work/sycamore_exp_project/src/data/D26.02.23_T19.51.56__" \
    "exp_0__shots_500000/amplitudes_n12_m14_s0_e0_pEFGH.txt",
    sep="\s+"
)

print(type(data))
print(dir(data))