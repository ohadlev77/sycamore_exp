import pandas as pd
import numpy as np

data_file_path = "google_chosen_data/n18_m14_s0_e0/amplitudes_n18_m14_s0_e0_pEFGH.txt"


raw_df = pd.read_csv(data_file_path, sep="\s+", dtype={"bitstring": str})
print()
print("RAW DF:")
print(raw_df)
print(raw_df["bitstring"])

curated_df = raw_df.copy(deep=True)
curated_df.drop_duplicates(inplace=True)
curated_df.sort_values("bitstring", inplace=True)
print()
print("CURATED DF")
print(curated_df)

for count, bitstring in enumerate(curated_df["bitstring"]):
    bin_count = format(count, "b").zfill(18)
    print(f"{bin_count}: {bitstring}")

    if bin_count != bitstring:
        curated_df.loc[count] = {"bitstring": bin_count, "real_amp": None, "imag_amp": None}
        break

print(curated_df)