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

def get_halo_distance(toxin_centre, blurred_plate, vertex, target_colour, halo_distances, halo_directions, halo_vertices, line_length):
    
    unit_vector = (vertex - toxin_centre) / np.linalg.norm(vertex - toxin_centre)

    t_values = np.linspace(0, line_length + 1, line_length)

    x_values = (vertex[0] + (unit_vector[0] * t_values)).astype(int)
    y_values = (vertex[1] + (unit_vector[1] * t_values)).astype(int)

    x_min, x_max = x_values[0], x_values[-1]
    y_min, y_max = y_values[0], y_values[-1]

    if x_max is None or y_max is None:
        print("x_max or y_max is None")
        return

    if y_min == y_max or x_min == x_max:
        # print("y_min equals y_max or x_min equals x_max")
        return

    if x_min < 0 or y_min < 0 or x_max >= blurred_plate.shape[1] or y_max >= blurred_plate.shape[0]:
        print("x or y values out of bounds")
        return

    colour_at_max = blurred_plate[x_max, y_max]

    if colour_at_max[0] != colour_at_max[1] or colour_at_max[0] != colour_at_max[2] and min(colour_at_max) > 0:
        
        print("Colour channels not equal or min colour > 0")
        return

    if target_colour <= 0:
        print("Target colour less than or equal to 0")
        return

    colours, distances = [], []

    averaging_circle_radius = 5
    averaging_mask_shape = ((averaging_circle_radius * 2) + 1, (averaging_circle_radius * 2) + 1)
    averaging_mask = np.zeros(averaging_mask_shape, dtype=np.uint8)

    for x, y in zip(x_values, y_values):
        averaging_region = blurred_plate[y - averaging_circle_radius:y + averaging_circle_radius + 1, x - averaging_circle_radius:x + averaging_circle_radius + 1]
        if averaging_region.shape[:2] != averaging_mask.shape:
            print("Averaging region shape mismatch")
            return
            
        masked_region_values = averaging_region[averaging_mask == 0]
        mean_region_colour = np.mean(masked_region_values)

        colours.append(mean_region_colour)
        distance_to_colour = np.sqrt((x - vertex[0]) ** 2 + (y - vertex[1]) ** 2)
        distances.append(distance_to_colour)

    toxin_radius = np.sqrt((vertex[0] - toxin_centre[0]) ** 2 + (vertex[1] - toxin_centre[1]) ** 2)
    toxin_glow = 0.25 * toxin_radius

    low_colour, high_colour = None, None

    for distance, colour in zip(distances, colours):
        if distance > toxin_glow:
            
            if colour < target_colour:
                low_colour = colour
                low_distance = distance
            
            if colour > target_colour and low_colour is not None:
                high_colour = colour
                high_distance = distance
    
                gradient = (high_colour - low_colour) / (high_distance - low_distance)
                intercept = high_colour - (gradient * high_distance)

                halo_distance = (target_colour - intercept) / gradient

                if halo_distance > toxin_glow:
                    halo_distances.append(halo_distance)
                    halo_directions.append(unit_vector)
                    halo_vertices.append(vertex)

                # # Graphing
                # colours = np.array(colours)
                # distances = np.array(distances)

                # plt.plot(distances, colours, color=cherry_hex, label='Halo Colour')
                # plt.axvline(x=halo_distance, color=tomato_hex, linestyle='--', label='Halo Distance')
                # plt.axhline(y=target_colour, color=blueberry_hex, linestyle='--', label='Target Colour')
                
                # plt.xlabel('Distance from toxin edge')
                # plt.ylabel('Pixel Intensity')
                # plt.legend()
                # plt.gca().spines['top'].set_visible(False)
                # plt.gca().spines['right'].set_visible(False)
                
                # plt.savefig("14_halo_distance.svg")
                # plt.show()

                break
