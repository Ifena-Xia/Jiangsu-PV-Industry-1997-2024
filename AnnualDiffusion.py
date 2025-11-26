# FIRST VERSION --- Same Value Y axis
'''
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_excel("diffusion_jiangsu.xlsx")

# Set up the figure
plt.figure(figsize=(8, 5))
plt.title("Jiangsu Photovoltaic Power Diffusion (2012–2020)", fontsize=14, weight='bold')

# Plot the two indicators
# Power Generation (100 GWh) — gold-ish yellow
plt.plot(df["Year"], df["Power Generation(100 GWh)"],
         color="#DAA520", linewidth=2.5, marker='o', label="Power Generation (100 GWh)")

# Installed Capacity (MW) — moderate steel blue
plt.plot(df["Year"], df["Installed capacity (MW)"],
         color="#4682B4", linewidth=2.5, marker='s', label="Installed Capacity (MW)")

# Add labels and grid
plt.xlabel("Year", fontsize=12)
plt.ylabel("Value", fontsize=12)
plt.grid(alpha=0.3)
plt.legend(frameon=False, fontsize=11)

# Beautify the layout
plt.tight_layout()

# Save the figure
plt.savefig("Diffusion_Jiangsu_PV.png", dpi=300, bbox_inches="tight")

# Show the chart
plt.show()
'''

# SECOND VERSION --- Dual Y axes
'''
import pandas as pd
import matplotlib.pyplot as plt

# Read your Excel file
df = pd.read_excel("diffusion_jiangsu.xlsx")

# Create the figure and the first axis
fig, ax1 = plt.subplots(figsize=(8, 5))

# --- Left Y-axis: Power Generation (gold-ish yellow) ---
ax1.plot(df["Year"], df["Power Generation(100 GWh)"],
         color="#DAA520", marker='o', linewidth=2.5,
         label="Power Generation (100 GWh)")
ax1.set_xlabel("Year", fontsize=12)
ax1.set_ylabel("Power Generation (100 GWh)", color="#DAA520", fontsize=12)
ax1.tick_params(axis='y', labelcolor="#DAA520")
ax1.grid(alpha=0.3)

# Add the second y-axis
ax2 = ax1.twinx()

# --- Right Y-axis: Installed Capacity (moderate steel blue) ---
ax2.plot(df["Year"], df["Installed capacity (MW)"],
         color="#4682B4", marker='s', linewidth=2.5,
         label="Installed Capacity (MW)")
ax2.set_ylabel("Installed Capacity (MW)", color="#4682B4", fontsize=12)
ax2.tick_params(axis='y', labelcolor="#4682B4")

# Title and layout
fig.suptitle("Jiangsu Photovoltaic Diffusion (2012–2020)",
             fontsize=14, weight='bold')
fig.tight_layout()
plt.savefig("Diffusion_Jiangsu_PV_dualaxis.png", dpi=300, bbox_inches="tight")

# Show the figure
plt.show()
'''

# THIRD VERSION --- Converting Units

import pandas as pd
import matplotlib.pyplot as plt

# Read your Excel file
df = pd.read_excel("diffusion_jiangsu.xlsx")

# Convert installed capacity from MW → GW
df["Installed capacity (GW)"] = df["Installed capacity (MW)"] / 1000

# Create the figure
fig, ax1 = plt.subplots(figsize=(8,5))

# --- Bars: Power Generation (gold) ---
ax1.bar(df["Year"].dropna(), df["Power Generation(100 GWh)"],
        color="#FFD700", alpha=0.75, label="Power Generation (100 GWh)")
# Handle missing data: draw grey slashed (hatched) bars
missing_label_added = False
for i, value in enumerate(df["Power Generation(100 GWh)"]):
    if pd.isna(value):
        ax1.bar(
            df["Year"][i],
            255,  # estimated height similar to 255
            color="lightgrey",
            edgecolor="grey",
            hatch="//",
            alpha=0.7,
            label="Estimated (missing)" if not missing_label_added else ""
        )
        missing_label_added = True

ax1.set_xlabel("Year", fontsize=12)
ax1.set_ylabel("Power Generation (100 GWh)", color="#B8860B", fontsize=12)
ax1.tick_params(axis='y', labelcolor="#B8860B")
ax1.grid(axis='y', alpha=0.3)

# Secondary axis for Installed Capacity (bold blue line)
ax2 = ax1.twinx()
ax2.plot(df["Year"], df["Installed capacity (GW)"],
         color="#1E3A8A", linewidth=3.2, marker='o',
         label="Installed Capacity (GW)")
ax2.set_ylabel("Installed Capacity (GW)", color="#1E3A8A", fontsize=12)
ax2.tick_params(axis='y', labelcolor="#1E3A8A")

# Title and layout
fig.suptitle("Jiangsu Photovoltaic Diffusion: Power Generation vs. Installed Capacity (2012–2020)",
             fontsize=14, weight='bold')
fig.tight_layout()
plt.savefig("Diffusion_Jiangsu_PV_barline.png", dpi=300, bbox_inches="tight")
plt.show()