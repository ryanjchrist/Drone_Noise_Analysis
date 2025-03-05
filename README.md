## Project Overview

This project is part of the Duke University Bass Connections research, focusing on developing optimal flight protocols for UAVs. The primary goal is to determine flight altitudes and speeds that minimize noise disturbances while ensuring effective data collection for monitoring african elephants.

## Dataset Description

The dataset consists of sound pressure level (SPL) measurements recorded at various altitudes using drone-mounted microphones. The data is gathered two audio text files collected and processed in 1/3 ocatave band by the microphone. This code utilizes two different vertical text files:

* 071124_1435_Ph4_A_V1_Audio_Text.txt

* 071124_1458_Ph4_A_V2_Audio_Text.txt

These files contain timestamped SPL data across multiple 1/3 octave frequency bands.

## Data Processing

### Data Import:

The two text files are read and parsed using pandas. Column headers are extracted from the first line, and the data is loaded while ensuring proper formatting.

Timestamps are converted to datetime objects for accurate time-based operations.

### Altitude Assignment:

Predefined altitude segments with their corresponding time intervals are used to assign altitude labels to each data point. A function get_altitude() maps each timestamp to its respective altitude based on the provided time windows.

### SPL Analysis:

SPL values are averaged for each frequency band at each altitude. The processed data is stored in mean_spl_per_altitude, a DataFrame where rows represent altitudes and columns represent the average SPL for each 1/3 octave frequency band.

## Visualization

### SPL vs. Frequency Plot:

A line plot is generated to compare SPL values across different altitudes. The x-axis represents the 1/3 octave frequency bands (Hz), and the y-axis represents the SPL (dB). Each altitude is represented with a unique color and marker.

### Selected Altitudes Comparison:

SPL distributions at key altitudes (10m, 40m, 70m, 120m) are plotted using subplots. Frequencies are converted to numerical values and sorted for a proper logarithmic x-axis scale. This visualization helps identify trends in noise attenuation at different altitudes.
