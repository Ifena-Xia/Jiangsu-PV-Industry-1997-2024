"""
Inputs (beside script): patent_counts_jiangsu.xlsx, diffusion_jiangsu.xlsx, operation_hours_jiangsu.xlsx
Deps: pandas, numpy, matplotlib, openpyxl
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, os
OUT="figs"; os.makedirs(OUT,exist_ok=True); PREFIX="jiangsu_pv"
INK="#121212"; MUTED="#6b6b6b"; GRID="#dcdcdc"
ACCENT="#2C6E49"      # dark green, the point color for PV
ACCENT2="#A7C9B5"     # light green
NEUTRAL="#9a9ea3"     # gray baseline
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"axes.edgecolor":INK,
    "axes.linewidth":0.8,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.7,
    "axes.axisbelow":True,"svg.fonttype":"none"})

def _frame(fig,title,subtitle,source):
    fig.text(0.065,0.965,title,ha="left",va="top",fontsize=15,fontweight="bold",color=INK)
    fig.text(0.065,0.915,subtitle,ha="left",va="top",fontsize=10.3,color=INK)
    fig.text(0.065,0.018,source,ha="left",va="bottom",fontsize=8.5,color=MUTED)
    fig.add_artist(plt.Line2D([0.065,0.115],[0.986,0.986],color=ACCENT,linewidth=3.2,solid_capstyle="butt"))

def fig_patents():
    p=pd.read_excel("patent_counts_jiangsu.xlsx",sheet_name="long_table")
    t=p.groupby("Year")["Count"].sum().reindex(range(1998,2025),fill_value=0)
    fig,ax=plt.subplots(figsize=(8.6,4.6)); fig.subplots_adjust(left=0.09,right=0.97,top=0.80,bottom=0.16)
    ax.axvspan(2007,2011,color=ACCENT2,alpha=0.45,zorder=0)
    ax.plot(t.index,t.values,color=ACCENT,linewidth=2.6,marker="o",markersize=3.5)
    ax.annotate("Peak: 108 (2011)",xy=(2011,108),xytext=(2013.2,99),fontsize=9.5,fontweight="bold",color=INK,
                arrowprops=dict(arrowstyle="-",color=MUTED,lw=0.8))
    ax.annotate("collapse after EU/US\nanti-dumping tariffs",xy=(2012,5),xytext=(2014.2,40),fontsize=8.8,color=MUTED,
                arrowprops=dict(arrowstyle="-",color=MUTED,lw=0.8))
    ax.text(2009,-15,"export-driven surge",ha="center",fontsize=8.6,color="#3c7d59",fontweight="bold")
    ax.set_xlim(1998,2024); ax.set_ylim(0,120); ax.set_ylabel("PV-related patent applications",fontsize=9.5)
    ax.spines[["top","right"]].set_visible(False)
    _frame(fig,"Innovation tracked the export boom, then fell with it",
        "PV-related patent applications in Jiangsu (CNIPA, IPC-filtered), total per year.",
        "Source: CNIPA Patent Search and Analysis platform, filtered by Jiangsu and PV-related IPC codes")
    for e in("svg","png"): fig.savefig(f"{OUT}/{PREFIX}_figPatents.{e}",dpi=200,bbox_inches="tight")
    plt.close(fig)

def fig_diffusion():
    d=pd.read_excel("diffusion_jiangsu.xlsx")
    d["cap_gw"]=d["Installed capacity (MW)"]/1000.0
    gen=d.dropna(subset=["Power Generation(100 GWh)"])
    fig,ax=plt.subplots(figsize=(8.8,4.8)); fig.subplots_adjust(left=0.09,right=0.90,top=0.80,bottom=0.16)
    ax.bar(gen["Year"],gen["Power Generation(100 GWh)"],color=ACCENT2,width=0.62,label="Power generation",zorder=2)
    ax.set_ylabel("Power generation (100 GWh)",fontsize=9.5,color="#3c7d59")
    ax.spines[["top"]].set_visible(False); ax.set_xlim(2011.4,2024.2)
    ax2=ax.twinx()
    ax2.plot(d["Year"],d["cap_gw"],color=ACCENT,linewidth=2.6,marker="o",markersize=3.5,label="Installed capacity",zorder=3)
    ax2.set_ylabel("Installed capacity (GW)",fontsize=9.5,color=ACCENT)
    ax2.spines[["top"]].set_visible(False); ax2.grid(False)
    ax.annotate("2019: generation falls while\ncapacity climbs (after the \u201c531\u201d cut)",xy=(2019,159),xytext=(2019.6,300),
                fontsize=8.6,color=MUTED,arrowprops=dict(arrowstyle="-",color=MUTED,lw=0.8))
    ax2.text(2021.0,d["cap_gw"].iloc[-1]-1.5,"installed\ncapacity",color=ACCENT,fontsize=8.8,va="center",fontweight="bold")
    _frame(fig,"Capacity kept climbing; output stumbled in 2019",
        "Jiangsu PV diffusion, 2012\u20132023. Bars: annual generation. Line: installed capacity. 2023 generation not yet reported.",
        "Source: China Electric Power Yearbooks (1998\u20132023 issues)")
    for e in("svg","png"): fig.savefig(f"{OUT}/{PREFIX}_figDiffusion.{e}",dpi=200,bbox_inches="tight")
    plt.close(fig)

def fig_hours():
    h=pd.read_excel("operation_hours_jiangsu.xlsx")
    fig,ax=plt.subplots(figsize=(8.0,4.4)); fig.subplots_adjust(left=0.10,right=0.96,top=0.80,bottom=0.16)
    ax.plot(h["Year"],h["Average Hours (h)"],color=ACCENT,linewidth=2.6,marker="o",markersize=4)
    ax.annotate("2018 \u201c531\u201d",xy=(2018,1059),xytext=(2018.1,1080),fontsize=8.8,color=MUTED)
    ax.set_ylim(1000,1320); ax.set_xlim(2015.6,2023.4); ax.set_ylabel("Average utilization hours",fontsize=9.5)
    ax.spines[["top","right"]].set_visible(False)
    _frame(fig,"Big stations held steady, so the squeeze fell on small ones",
        "Average annual utilization hours of PV stations \u22656 MW in Jiangsu, 2016\u20132023. Stable hours for centralized plants imply distributed PV bore the subsidy withdrawal.",
        "Source: China Electric Power Yearbooks")
    for e in("svg","png"): fig.savefig(f"{OUT}/{PREFIX}_figHours.{e}",dpi=200,bbox_inches="tight")
    plt.close(fig)

if __name__=="__main__":
    fig_patents(); fig_diffusion(); fig_hours()
    print("Wrote figures with prefix",PREFIX)
