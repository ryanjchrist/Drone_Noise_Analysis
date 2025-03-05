import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import timedelta

file1 = "071124_1435_Ph4_A_V1_Audio_Text.txt"
with open(file1, "r") as f:
    lines1 = f.readlines()

columns = lines1[0].strip().split("\t")

data1 = pd.read_csv(file1, delimiter="\t", skiprows=1, names=columns)

data1["point"] = data1["point"].str.strip(" ")
data1["timestamp"] = pd.to_datetime(data1["point"], format="%H:%M:%S.%f")

file2 = "071124_1458_Ph4_A_V2_Audio_Text.txt"
with open(file2, "r") as f:
    lines2 = f.readlines()

columns2 = lines2[0].strip().split("\t")

data2 = pd.read_csv(file2, delimiter="\t", skiprows=1, names=columns2)

data2["point"] = data2["point"].str.strip(" ")
data2["timestamp"] = pd.to_datetime(data2["point"], format="%H:%M:%S.%f")

data = pd.concat([data1, data2], ignore_index=True)

data = data.sort_values(by="timestamp")

altitude_data = [
    (120, "14:39:00"), (115, "14:40:00"), (110, "14:41:30"), (105, "14:42:15"),
    (100, "14:42:56"), (95, "14:43:41"), (90, "14:44:25"), (85, "14:45:09"),
    (80, "14:45:51"), (75, "14:46:30"), (70, "14:47:10"), (65, "14:47:54"),
    (60, "14:48:38"), (55, "14:59:19"), (50, "15:02:46"), (45, "15:03:32"), 
    (40, "15:04:15"), (35, "15:04:55"), (30, "15:05:38"), (25, "15:06:20"),
    (20, "15:07:04"), (15, "15:07:50"), (10, "15:08:34")
]

altitudes = pd.DataFrame(altitude_data, columns=["Altitude", "Time"])
altitudes["Start Time"] = pd.to_datetime(altitudes["Time"], format="%H:%M:%S")
altitudes["End Time"] = altitudes["Start Time"] + timedelta(seconds=30)

def get_altitude(timestamp):
    for _, row in altitudes.iterrows():
        if row["Start Time"] <= timestamp <= row["End Time"]:
            return row["Altitude"]
    return None

data["Altitude"] = data["timestamp"].apply(get_altitude)

frequency_bands = [col for col in data.columns if "1/3 Octave" in col]
mean_spl_per_altitude = data.groupby("Altitude")[frequency_bands].mean()
print(mean_spl_per_altitude)

plt.figure(figsize=(12, 8))
for altitude, row in mean_spl_per_altitude.iterrows():
    plt.plot(frequency_bands, row, marker = "o", label=f"{altitude}m")

plt.xlabel("1/3 Octave Frequency Bands (Hz)")
plt.ylabel("SPL (dB)")
plt.title("SPL vs. Frequency at Different Altitudes")
plt.legend(title="Altitude (m)")
plt.xticks(rotation=90)
plt.grid()
plt.show()


selected_altitudes = [10, 40, 70, 120]

frequency_bands = [col for col in data.columns if "1/3 Octave" in col]
mean_spl_per_altitude = data.groupby("Altitude")[frequency_bands].mean()
mean_spl_selected = mean_spl_per_altitude.loc[selected_altitudes]

frequencies = []
valid_columns = []
for col in frequency_bands:
    match = re.search(r"(\d+\.?\d*)\s*(Hz|kHz)", col)
    if match:
        freq = float(match.group(1))
        unit = match.group(2)
        if unit == "kHz":
            freq *= 1000
        frequencies.append(freq)
        valid_columns.append(col)

frequencies = np.array(frequencies)

sorted_indices = np.argsort(frequencies)
frequencies = frequencies[sorted_indices]
valid_columns = [valid_columns[i] for i in sorted_indices]

fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharey=True)
axes = axes.flatten()

for i, altitude in enumerate(selected_altitudes):
    ax = axes[i]
    ax.plot(frequencies, mean_spl_selected.loc[altitude, valid_columns], marker="o", label=f"{altitude}m")

    ax.set_xscale("log")
    ax.set_title(f"{altitude}m")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)

fig.supylabel("SPL (dB)")
fig.supxlabel("Frequency (Hz) Logrithmic Scale")
plt.tight_layout()
plt.show()
