# Annual Average Utilization Hours of Power Plants with an Installed Capacity of 6 MW or above

import pandas as pd
import matplotlib.pyplot as plt

# Read your Excel file
df = pd.read_excel("operation_hours_jiangsu.xlsx")

# Create the figure
fig, ax1 = plt.subplots(figsize=(8,5))

ax1.plot(df["Year"], df["Average Hours (h)"],
         color="#9C3C38", linewidth=3.5, marker='o',
         label="Average Hours (h)")
ax1.set_xlabel("Year", fontsize=12)
ax1.set_ylabel("Average Hours (h)", color="#3D0C02", fontsize=12)
ax1.tick_params(axis='y', labelcolor="#3D0C02")
ax1.grid(axis='y', alpha=0.3)

# Adjust y-axis range (flatten fluctuations)
y_min = df["Average Hours (h)"].min()
y_max = df["Average Hours (h)"].max()

# Add a buffer to compress variation visually
ax1.set_ylim(y_min - 30, y_max + 30)

fig.suptitle("Annual Average Utilization Hours of Power Plants with an Installed Capacity of 6 MW or above (2016–2023)",
             fontsize=14, weight='bold')
fig.tight_layout()
plt.savefig("Operation_Jiangsu_PV_hour_adjusted.png", dpi=300, bbox_inches="tight")
plt.show()