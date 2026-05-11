import numpy as np
from HaloUMI_functions._00_statistics import statistics

import matplotlib.pyplot as plt
blueberry_hex, blueberry_rgb = "#96AAFA", (150,170,250)
cherry_hex, cherry_rgb = "#A03C6E", (160,60,110)
honeydew_hex, honeydew_rgb = "#64d2be", (100, 210, 190)
tomato_hex, tomato_rgb = "#F04650", (240,70,80)
grape_hex, grape_rgb = "#7846C8", (120,70,200)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Verdana'
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["savefig.pad_inches"] = 0
plt.rcParams["savefig.dpi"] = 600

def get_target_colour(rgb_plate, lawn_ring_vertices, deadzone_ring_vertices, check):

    lawn_polygon = np.array(lawn_ring_vertices, dtype=np.int32)    
    lawn_colours = [rgb_plate[y, x] for x, y in lawn_polygon]
    deadzone_polygon = np.array(deadzone_ring_vertices, dtype=np.int32)
    deadzone_colours = [rgb_plate[y, x] for x, y in deadzone_polygon]

    mean_lawn, stdev_lawn, lower_bound_lawn, upper_bound_lawn = statistics(lawn_colours, 1)
    mean_deadzone, stdev_deadzone, lower_bound_deadzone, upper_bound_deadzone = statistics(deadzone_colours, 1)

    if check:
        target_colour = int((mean_deadzone + mean_lawn) / 2)

    elif upper_bound_deadzone < lower_bound_lawn and stdev_lawn/mean_lawn < 0.25:
        target_colour = int((mean_deadzone + mean_lawn) / 2)
        
    else:
        target_colour = 0

    # # Graphing
    # lawn_colours = np.array(lawn_colours)
    # deadzone_colours = np.array(deadzone_colours)

    # lawn_min, lawn_max = lawn_colours[:, 0].min(), lawn_colours[:, 0].max()
    # deadzone_min, deadzone_max = deadzone_colours[:, 0].min(), deadzone_colours[:, 0].max()

    # lawn_bins = (lawn_max - lawn_min) // 4
    # deadzone_bins = (deadzone_max - deadzone_min) // 4

    # plt.hist(lawn_colours[:, 0], bins=lawn_bins, color=cherry_hex, alpha=0.3, label='Lawn Ring Intensity Frequency')
    # plt.hist(deadzone_colours[:, 0], bins=deadzone_bins, color=honeydew_hex, alpha=0.5, label='Deadzone Ring Intensity Frequency')
    # plt.axvline(x=mean_lawn, color=cherry_hex, linestyle='--', label='Mean Lawn Colour', linewidth=3)
    # plt.axvline(x=mean_deadzone, color=honeydew_hex, linestyle='--', label='Mean Deadzone Colour', linewidth=3)
    # plt.axvline(x=target_colour, color=blueberry_hex, linestyle='--', label='Target Colour', linewidth=3)

    # plt.xlim(right=255)

    # plt.xlabel('Pixel Intensity')
    # plt.ylabel('Frequency')
    # plt.legend()
    # plt.gca().spines['top'].set_visible(False)
    # plt.gca().spines['right'].set_visible(False)

    # plt.savefig("13_target-colour.svg")
    # plt.show()

    return target_colour