import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

workbook_path = r"T:\rsrch\cm1746\lab\Archived Raw Data\Plate Scanning\Alex\2026_07_13_testing\HaloUMI_output.xlsx"
workbook_file = pd.ExcelFile(workbook_path)

colours = [["#E0D252","#E0A752","#E07C52","#E05252"],
           ["#52E0B6","#52E060","#99E052","#C4E052"],
           ["#5260E0","#528BE0","#52B6E0","#52E0E0"],
           ["#E052D2","#C452E0","#9952E0","#6E52E0"]]

marker_types = ['o', 's', '^', 'D']

y_ranges = [[2000,9500],
            [2500,9500],
            [3000,11500],
            [2500,10500]
            ]

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Verdana'
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["savefig.pad_inches"] = 0
plt.rcParams["savefig.dpi"] = 600
plt.rcParams['font.size'] = 36

count = 0

#log_lc, log2_σ_vis, log2_σ_vis
x_axis = "log_tc"

#r, r^2, r^2_corr
y_axis = "r"

filetype = "both"

tox_or_conc = "tox"

for sheet_name in workbook_file.sheet_names:
    
    if tox_or_conc == "tox":
        changes = ["t1", "t2", "t3", "t4"]
        name_check = True
    else:
        changes = ["l1", "l2", "l3", "l4"]
        name_check = False

    if ("plate" in sheet_name) == name_check:
        plt.figure(figsize=(8, 8))
        df = pd.read_excel(workbook_path, sheet_name=sheet_name)
        if tox_or_conc == "tox":
            changes = ["t1", "t2", "t3", "t4"]
        else:
            changes = ["l1", "l2", "l3", "l4"]    
        x_axis_averages,y_axis_averages= [], []
        for c,change in enumerate(changes):
            
            condition = df.astype(str).apply(lambda x: x.str.contains(change, case=False)).any(axis=1)
            filtered_df = df[condition]

            spots = ["s1", "s2", "s3", "s4"]
            if not filtered_df.empty:

                for s, spot in enumerate(spots):

                    try:
                        condition = filtered_df.astype(str).apply(lambda x: x.str.contains(spot, case=False)).any(axis=1)
                        spot_df = filtered_df[condition]


                        if not spot_df.empty:

                            x_average = np.mean(spot_df[x_axis])
                            y_average = np.mean(spot_df[y_axis])
                            y_stdev = np.std(spot_df[y_axis])

                            color = colours[count][c] if tox_or_conc == "conc" else colours[c][count]
                            if spot == "s1":
                                plt.scatter(
                                    spot_df[x_axis],
                                    spot_df[y_axis],
                                    color=color,
                                    alpha=0.03)
                                
                                plt.errorbar(x=x_average,
                                            y=y_average,
                                            yerr=y_stdev,
                                            color=color,
                                            alpha=1,
                                            marker=marker_types[c],
                                            markersize=9,
                                            label=change)                            
                            else:
                                plt.scatter(
                                    spot_df[x_axis],
                                    spot_df[y_axis],
                                    color=color,
                                    alpha=0.03)
                            
                                plt.errorbar(x=x_average,
                                            y=y_average,
                                            yerr=y_stdev,
                                            color=color,
                                            alpha=1,
                                            marker=marker_types[c],
                                            markersize=9)


                        
                            if not (np.isnan(x_average) or np.isnan(y_average)):
                        
                                x_axis_averages.append(x_average)
                                y_axis_averages.append(y_average)
                        else:
                            print(f"Spot {spot} in Lawn {change} was empty.")
                    except:
                        print(f"No spot #{s+1}")

        if len(x_axis_averages) > 1:

            k, c = np.polyfit(x=x_axis_averages,
                                y=y_axis_averages,
                                deg=1)
            
            xseq = np.linspace(min(x_axis_averages), max(x_axis_averages), num=100)
            plt.plot(xseq, c+(k*xseq), color="k", linestyle="--")
            if x_axis == "log_lc":
                plt.xlabel(r'$\log_2$(Lawn OD)')

            elif x_axis == "log_tc":
                plt.xlabel(r'$\log_2$(Lawn OD)', fontsize=36)
                

            else:
                plt.xlabel(r'$\log_2(\sigma_{\mathrm{vis}})$')

            if y_axis == "r":
                ax = plt.gca()

                ax.set_ylabel("Halo Distance", rotation=270, labelpad=15, va="bottom")
                ax.yaxis.set_label_position("right")

                ax.yaxis.tick_right()

                # ax.set_ylabel("Halo Distance")
                # leg = plt.legend(loc='upper right') if tox_or_conc == "conc" else plt.legend(loc='upper left')
                plt.ylim(42.5,107.5)
            else:
                plt.ylabel("Halo Distance Squared")
                # leg = plt.legend(loc='lower right')

                plt.ylim(2000, 11500)
            
            # for lh in leg.legend_handles: 
            #     lh.set_alpha(1.0)

            

            # plt.title(f"{k}")

        else:
            plt.title(f"Sheet: {sheet_name} (Not enough points to fit trendline)")

        print(f"{c+1}_{k}")
        if y_axis == "r":
            if tox_or_conc == "tox":
                fig_key = "r_vs_lawn"
            else:
                fig_key = "r_vs_tox"
        elif y_axis == "r^2":
            fig_key = "uncorrected"
        else:
            fig_key = "corrected"

        naming = "l" if tox_or_conc == "tox" else "t"

        if filetype == "both":
            plt.savefig(f"{naming}{count+1}_{fig_key}.svg")
            plt.savefig(f"{naming}{count+1}_{fig_key}.png")

        else:
            plt.savefig(f"{naming}{count+1}_{fig_key}.{filetype}")

        plt.close()
        count += 1




# filtered_dfs = []

# for sheet_name in workbook_file.sheet_names:

#     if "plate" in sheet_name:
#         df = pd.read_excel(workbook_path, sheet_name=sheet_name)
#         look_for = "t4"

#         condition = df.astype(str).apply(lambda x: x.str.contains(look_for, case=False)).any(axis=1)
#         filtered_df = df[condition]

#         if not filtered_df.empty:
#             filtered_dfs.append(filtered_df)

# if filtered_dfs:
#     final_df = pd.concat(filtered_dfs, ignore_index=True)

#     with pd.ExcelWriter(workbook_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
#             final_df.to_excel(writer, sheet_name=look_for, index=False)
            
#     print(f"Success! The matching rows have been saved to the '{look_for}' sheet.")
# else:
#     print("No rows containing 'apple' were found in any of the sheets.")
    