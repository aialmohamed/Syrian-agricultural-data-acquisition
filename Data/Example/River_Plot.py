import xarray as xr
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

# === 1. Load Dataset ===

# Directory containing your monthly .nc files
folder = "A:/Work/SGRD/Smart_Farming/Project_Pilot_and_Main_Docs/euphrates_precipitation"

# Combine all NetCDF files
ds = xr.open_mfdataset(
    os.path.join(folder, "*.nc"),
    combine="by_coords",
    engine="netcdf4"
)

# === 2. Calculate Monthly Mean Over Area ===
monthly_avg = ds['precipitation'].mean(dim=['lat', 'lon'])

# === 3. Calculate PON ===
mean_precip = monthly_avg.mean()
pon = (monthly_avg / mean_precip) * 100

# Convert to pandas Series for classification
pon_series = pon.to_series()

# === 4. Classify PON Values ===
pon_class = pd.Series(index=pon_series.index, dtype="str")
pon_class[pon_series < 75] = "Below Normal"
pon_class[(pon_series >= 75) & (pon_series <= 125)] = "Normal"
pon_class[pon_series > 125] = "Above Normal"

# === 5. Color Coding ===
colors = pon_series.copy().astype(str)
colors[pon_series < 75] = "red"
colors[(pon_series >= 75) & (pon_series <= 125)] = "gold"
colors[pon_series > 125] = "green"

# === 6. Plotting ===
pon_capped = pon_series.clip(upper=200)

plt.figure(figsize=(14, 5))
plt.bar(pon_series.index, pon_capped, color=colors)
plt.axhline(100, color='gray', linestyle='--', label="Normal (100%)")
plt.title("Percentage of Normal (PON) — Precipitation Classification (Capped at 200%)")
plt.ylabel("PON (%)")
plt.xlabel("Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# === 7. Optional: Export to CSV ===
#result_df = pd.DataFrame({
#    "Time": pon_series.index,
#    "PON (%)": pon_series.values,
#    "Category": pon_class.values
#})

#result_df.to_csv("precipitation_pon_classification.csv", index=False)
