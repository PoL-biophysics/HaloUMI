import cv2 as cv
import matplotlib as mpl
import numpy as np
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

def get_valid_halos(halo_distance, halo_index, mean_halo, stdev_halo, lower_bound_halo, upper_bound_halo, valid_halos, valid_anorms, valid_dirs, valid_vers, halo_directions, halo_vertices, allow_outliers, polygon_area, halo_distances):
    
#    # Graphing

#     from scipy.stats import norm

#     count, bins, ignored = plt.hist(halo_distances, bins=40, density=True, 
#                                     color=honeydew_hex, alpha=0.4, label='Halo Distance Frequency')

#     x = np.linspace(min(halo_distances), max(halo_distances), 1000)
#     p = norm.pdf(x, mean_halo, stdev_halo)
#     plt.plot(x, p, color=tomato_hex, linewidth=2, label='Normal Distribution')
#     plt.axvline(x=mean_halo, color=grape_hex, linestyle='--', label='Mean Halo Distance')
#     plt.axvline(x=lower_bound_halo, color=blueberry_hex, linestyle='--', label='±1σ')
#     plt.axvline(x=upper_bound_halo, color=blueberry_hex, linestyle='--')

#     plt.xlabel('Halo Distance')
#     plt.ylabel('Probability Density')

#     plt.gca().spines['top'].set_visible(False)
#     plt.gca().spines['right'].set_visible(False)

#     plt.legend()
#     plt.savefig("15_halo-distance-distribution.svg")
#     plt.show()    
    
    if lower_bound_halo < halo_distance < upper_bound_halo and stdev_halo/mean_halo < 0.25:
        valid_halo_distance = halo_distance
        valid_halo_anorm = halo_distance / (polygon_area ** 0.5)
        valid_halo_direction = halo_directions[halo_index]
        valid_halo_vertex = halo_vertices[halo_index]

        valid_halos.append(valid_halo_distance)
        valid_anorms.append(valid_halo_anorm)
        valid_dirs.append(valid_halo_direction)
        valid_vers.append(valid_halo_vertex)

        boolean = True

        return boolean, valid_halo_distance, valid_halo_anorm, valid_halo_direction, valid_halo_vertex

    else:

        invalid_halo_distance = halo_distance
        invalid_halo_anorm = halo_distance / (polygon_area ** 0.5)
        invalid_halo_direction = halo_directions[halo_index]
        invalid_halo_vertex = halo_vertices[halo_index]

        if allow_outliers:

            valid_halos.append(invalid_halo_distance)
            valid_anorms.append(invalid_halo_anorm)
            valid_dirs.append(invalid_halo_direction)
            valid_vers.append(invalid_halo_vertex)

        boolean = False


        return boolean, invalid_halo_distance, invalid_halo_anorm, invalid_halo_direction, invalid_halo_vertex
