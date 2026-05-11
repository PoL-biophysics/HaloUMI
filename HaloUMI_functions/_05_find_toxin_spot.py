import numpy as np
import cv2 as cv
from scipy.spatial import distance

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

def find_toxin_spot(contour, rgb_plate, all_toxin_vertices, toxin_centres, polygon_areas, epsilon_f, min_area_f, max_area_f, ratio_tolerance):

    perimeter = cv.arcLength(contour, True)
    epsilon = epsilon_f * perimeter
    polygon_vertices = cv.approxPolyDP(contour, epsilon, True)
    polygon_area = cv.contourArea(polygon_vertices)
    diameter = ((polygon_area / np.pi) ** 0.5) * 2
    _, _, w, h = cv.boundingRect(polygon_vertices)

    plate_area = rgb_plate.shape[0] * rgb_plate.shape[1]
    min_area, max_area = (plate_area * min_area_f), (plate_area * max_area_f)
    valid_area = min_area < polygon_area < max_area

    valid_diameter_to_height = (1/ratio_tolerance) < (diameter/h) < ratio_tolerance
    valid_diameter_to_width = (1/ratio_tolerance) < (diameter/w) < ratio_tolerance
    valid_width_to_height = (1/ratio_tolerance) < (h/w) < ratio_tolerance
    is_circular = valid_diameter_to_height and valid_diameter_to_width and valid_width_to_height

    is_valid_contour = valid_area and is_circular
     
    if is_valid_contour:

        M = cv.moments(polygon_vertices)
        if M["m00"] != 0:
            centre_x = int(M["m10"] / M["m00"])
            centre_y = int(M["m01"] / M["m00"])
            centre = (centre_x, centre_y)
            new_check = False
            if centre_x < 1000 and centre_y > 1000:
                new_check = True

            new_check = True # temporary override
            spot_separation = 10
            if all(distance.euclidean(centre, prev_centre) > spot_separation for prev_centre in toxin_centres) and new_check:
                all_toxin_vertices.append(polygon_vertices)
                toxin_centres.append(centre)
                polygon_areas.append(polygon_area)

                # cv.circle(rgb_plate, (centre_x, centre_y), 5, blueberry_rgb, -1)
                cv.drawContours(rgb_plate, [polygon_vertices], -1, (0,0,0), 5)
                
                # # Graphing
                
                # plt.imshow(rgb_plate)
                # plt.savefig("11_detected-toxin-spot.svg")
                # plt.close()

                # # mark on vertices in green
                # for vertex in polygon_vertices:
                #     cv.circle(rgb_plate, (vertex[0][0], vertex[0][1]), 3, (0,255,0), -1)
                    

                return polygon_vertices, centre, polygon_areas, is_valid_contour
            
            print("not separated enough")
        
        print("problem with center")

    # elif valid_area:
    #     cv.drawContours(rgb_plate, [polygon_vertices], -1, (200, 100, 50), 5)
    #     # print(f"Area: {polygon_area}, d:h - {(diameter/h)}, d:w - {(diameter/w)}, h:w - {(h/w)}")

    # elif is_circular:
    #     cv.drawContours(rgb_plate, [polygon_vertices], -1, (50, 100, 200), 5)
    #     # print(f"Area: {polygon_area}, d:h - {(diameter/h)}, d:w - {(diameter/w)}, h:w - {(h/w)}")

    # elif min_area < polygon_area:
    #     cv.drawContours(rgb_plate, [polygon_vertices], -1, (250, 100, 200), 5)
    #     # print(f"Area: {polygon_area}, d:h - {(diameter/h)}, d:w - {(diameter/w)}, h:w - {(h/w)}")
            
    return [], [], [], False