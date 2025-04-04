import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
from datetime import timedelta

files = ["New File-32.txt", "New File-33.txt", "New File-36.txt"]

altitude_mappings = {
    "New File-32.txt": [
        (100, "11:21:01"), (95, "11:21:31"), (90, "11:21:58"), (85, "11:22:34"),
        (80, "11:23:05"), (75, "11:23:34"), (70, "11:24:10"), (65, "11:24:48"),
        (60, "11:25:18"), (55, "11:25:56"), (50, "11:26:26"), (45, "11:26:57"), 
        (40, "11:27:26"), (35, "11:27:59"), (30, "11:28:28"), (25, "11:28:56"),
        (20, "11:29:31"), (15, "11:30:05")
    ],
    "New File-33.txt": [
        (100, "11:38:31"), (95, "11:39:01"), (90, "11:39:29"), (85, "11:40:00"),
        (80, "11:40:27"), (75, "11:41:00"), (70, "11:41:38"), (65, "11:42:09"),
        (60, "11:42:40"), (55, "11:43:11"), (50, "11:43:38"), (45, "11:44:13"), 
        (40, "11:44:41"), (35, "11:45:29"), (30, "11:46:08"), (25, "11:46:39"),
        (20, "11:47:08"), (15, "11:47:42")
    ],
    "New File-36.txt": [
        (100, "12:35:15"), (95, "12:35:44"), (90, "12:36:12"), (85, "12:36:51"),
        (80, "12:37:18"), (75, "12:37:55"), (70, "12:38:20"), (65, "12:38:51"),
        (60, "12:39:20"), (55, "12:39:47"), (50, "12:40:16"), (45, "12:40:41"), 
        (40, "12:41:18"), (35, "12:41:50"), (30, "12:42:20"), (25, "12:42:51"),
        (20, "12:43:16"), (15, "12:43:43")
    ]
}
all_data = []

for file in files:
    with open(file, "r") as f:
        lines = f.readlines()
    
    columns = lines[0].strip().split("\t")
    data = pd.read_csv(file, delimiter="\t", skiprows=1, names=columns)

    data["point"] = data["point"].str.strip()
    data["timestamp"] = pd.to_datetime(data["point"], format="%H:%M:%S.%f")

    data = data.sort_values(by="timestamp")

    altitudes = pd.DataFrame(altitude_mappings[file], columns=["Altitude", "Time"])
    altitudes["Start Time"] = pd.to_datetime(altitudes["Time"], format="%H:%M:%S") + timedelta(seconds=1)
    altitudes["End Time"] = altitudes["Start Time"] + timedelta(seconds=10)

    def get_altitude(timestamp):
        for _, row in altitudes.iterrows():
            if row["Start Time"] <= timestamp <= row["End Time"]:
                return row["Altitude"]
        return None

    data["Altitude"] = data["timestamp"].apply(get_altitude)
    
    all_data.append(data)

combined_data = pd.concat(all_data, ignore_index=True)

frequency_bands = [col for col in combined_data.columns if "1/3 Octave" in col]

mean_spl_per_altitude = combined_data.groupby("Altitude")[frequency_bands].mean()

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 8))
palette = sns.color_palette("viridis_r", n_colors=len(mean_spl_per_altitude))

for (altitude, row), color in zip(mean_spl_per_altitude.iterrows(), palette):
    sns.lineplot(x=frequency_bands, y=row, marker="o", label=f"{altitude}m", color=color)

plt.xlabel("1/3 Octave Frequency Bands (Hz)")
plt.ylabel("SPL (dB)")
plt.title("Averaged SPL vs. Frequency at Different Altitudes")
plt.legend(title="Altitude (m)", loc="upper right", bbox_to_anchor=(1, 1), fontsize=10)

short_labels = [re.search(r"(\d+\.?\d*)\s*(Hz|kHz)", col).group(0) for col in frequency_bands]

plt.xticks(ticks=range(len(short_labels)), labels=short_labels, rotation=45)
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

selected_altitudes = [15, 40, 70, 100]
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
    sns.lineplot(x=frequencies, y=mean_spl_selected.loc[altitude, valid_columns], marker="o", ax=ax)
    ax.set_xscale("log")
    ax.set_ylabel("")
    ax.set_title(f"{altitude}m")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)

fig.supylabel("SPL (dB)")
fig.supxlabel("Frequency (Hz) Logarithmic Scale")
plt.tight_layout()
plt.show()
