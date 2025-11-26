# --- 0) Imports
import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- 1) Paste your four IPC text blocks exactly as you copied them
txt_H01L31 = """
2023 1 item, 2021 1 item, 2019 1 item, 2014 1 item, 2013 1 item,
2010 1 item, 2009 1 item, 2008 2 items, 2007 2 items, 2006 1 item,
2004 1 item, 2002 1 item
""".strip()

txt_H01L21 = """
2024 1 item, 2023 4 items, 2022 2 items, 2021 4 items, 2020 1 item,
2019 2 items, 2018 2 items, 2017 2 items, 2015 2 items, 2014 6 items,
2013 5 items, 2012 3 items, 2011 106 items, 2010 63 items, 2009 61 items,
2008 30 items, 2007 19 items, 2006 6 items, 2005 8 items, 2004 8 items,
2003 2 items, 2002 4 items, 2001 2 items, 1998 3 items
""".strip()

txt_C30B29 = """
2011 2 items, 2009 1 item, 2008 1 item, 2007 1 item, 2000 1 item
""".strip()

txt_C01B33 = """
2023 3 items, 2022 1 item, 2020 2 items, 2019 1 item, 2018 1 item,
2015 2 items, 2013 1 item, 2012 2 items, 2009 6 items, 2005 1 item
""".strip()

# --- 2) Helper to parse "YYYY N item(s)" into a DataFrame for one IPC
def parse_ipc_block(text_block: str, ipc_code: str) -> pd.DataFrame:
    # Matches patterns like "2011 106 items" or "2008 1 item"
    pairs = re.findall(r'(\d{4})\s+(\d+)\s+item', text_block)
    df = pd.DataFrame(pairs, columns=["Year", "Count"]).astype({"Year": int, "Count": int})
    df["IPC"] = ipc_code
    return df.sort_values("Year").reset_index(drop=True)

# --- 3) Build the long table
dfs = [
    parse_ipc_block(txt_H01L31, "H01L 31/00"),
    parse_ipc_block(txt_H01L21, "H01L 21/00"),
    parse_ipc_block(txt_C30B29, "C30B 29/00"),
    parse_ipc_block(txt_C01B33, "C01B 33/00"),
]
long_df = pd.concat(dfs, ignore_index=True)

# --- 4) Sanity checks to avoid silent mistakes
# - No negative counts
assert (long_df["Count"] >= 0).all()
# - Years look reasonable for your study window
assert long_df["Year"].between(1990, 2030).all()

# --- 5) Produce wide and totals
wide_df = long_df.pivot_table(index="Year", columns="IPC", values="Count", aggfunc="sum").fillna(0).astype(int)
wide_df["Total"] = wide_df.sum(axis=1)
wide_df = wide_df.sort_index()

# --- 6) Ensure continuous years if you want a smooth axis (optional)
full_years = pd.Index(range(wide_df.index.min(), wide_df.index.max() + 1), name="Year")
wide_df = wide_df.reindex(full_years, fill_value=0)

# --- 7) Save to Excel with multiple sheets
out_xlsx = Path("patent_counts_jiangsu.xlsx")
with pd.ExcelWriter(out_xlsx, engine="xlsxwriter") as xw:
    long_df.to_excel(xw, sheet_name="long_table", index=False)
    wide_df.reset_index().to_excel(xw, sheet_name="wide_with_total", index=False)

print(f"Excel saved → {out_xlsx.resolve()}")

# --- 8) Make a jade-green line chart for Total by Year
plt.figure(figsize=(9, 4.8))
jade = "#00A86B"
plt.plot(wide_df.index, wide_df["Total"], marker="o", linewidth=2.5, markersize=5.5, color=jade)

# Highlight 2006–2011
plt.axvspan(2006, 2011, color=jade, alpha=0.08)

# Label peak
peak_year = int(wide_df["Total"].idxmax())
peak_val = int(wide_df.loc[peak_year, "Total"])
plt.annotate(
    f"Peak {peak_val} (2011)",
    xy=(peak_year, peak_val),
    xytext=(peak_year - 4, peak_val * 0.9),
    arrowprops=dict(arrowstyle="->", color=jade),
    fontsize=10,
)

plt.title("PV-related Patents in Jiangsu (CNIPA, IPC-filtered)")
plt.xlabel("Year")
plt.ylabel("Total PV-related Patents")
plt.grid(axis="y", alpha=0.25)
plt.tight_layout()
plt.savefig("patent_trend_jade.png", dpi=300)
plt.show()
print("Figure saved →", Path("patent_trend_jade.png").resolve())

# --- 9) Print a quick preview of totals
print("\nTotals by year:")
print(wide_df["Total"].to_string())