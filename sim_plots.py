import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Verdana'
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["savefig.pad_inches"] = 0
plt.rcParams["savefig.dpi"] = 600
plt.rcParams['font.size'] = 18

spreadsheet_path = r"G:\My Drive\alex_pembery_ELN\01_chapters\chpt05_trafficking_pathways\HaloUMI\other_HaloUMI\2026_02_05_HaloUMI_output.xlsx"

df = pd.read_excel(spreadsheet_path)

columns = ["regular", "irregular", "gradient", "smallest", "blips", "real"]

my_palette = {"regular": "#777777", "irregular": "#96aafa", "gradient": "#a03c6e", "smallest": "#BBBBBB", "blips": "#f04650", "real": "#7846c8"}

sns.violinplot(data=df[columns], palette=my_palette)

x = [0,1,2,3,4,5]
y= [135.8, 90, 101.1, 30.1, 135.8, 135.8]

plt.scatter(x,y, color="#64d2be", marker='D', s=50, label="Theoretical Value")
# plt.xlabel("Simulation Variant")
plt.ylabel("Halo Distance (px)")


plt.tight_layout()
plt.legend(loc='lower right')
plt.show()

