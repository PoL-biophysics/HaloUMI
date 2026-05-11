# %%

import cv2 as cv
import os
import tkinter as tk
import numpy as np
import pandas as pd
import openpyxl
import tkinter as tk
import matplotlib as mpl
import math
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import filedialog, simpledialog
from matplotlib import pyplot as plt
from pathlib import Path
from matplotlib.widgets import Slider, TextBox, CheckButtons
from datetime import date, datetime

os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

# functions
from HaloUMI_functions import (
    statistics,
    preprocess_image,
    find_plates,
    find_peaks_in_plate,
    image_thresholding,
    find_toxin_spot,
    find_rings,
    get_target_colour,
    get_halo_distance,
    get_valid_halos,
)


# get the current day of the year
day = datetime.today().timetuple().tm_yday

def get_season(day):
    if 59 <= day < 152:
        season = 'spring'
    elif 152 <= day < 244:
        season = 'summer'
    elif 244 <= day < 334:
        season = 'autumn'
    else:
        season = 'winter'
    return season

cmap_c = get_season(day)

def HaloUMI_main(folder_name, file):
    
    image_path = os.path.join(folder_name, file)

    grey_image, resized_image = preprocess_image(image_path, scale=0.1)

    plates = find_plates(resized_image, scale=0.1)
    plate_radius = plates[0,0,2]

    for p, plate in enumerate(plates[0,:]):
        try:
            black_peak, grey_peak, white_peak, grey_plate = find_peaks_in_plate(grey_image, plate, plate_radius)
            between_peaks = (grey_peak + white_peak) // 2
            rgb_plate, contours = image_thresholding(black_peak, grey_peak, white_peak, grey_plate, between_peaks)
            blank_plate = rgb_plate.copy()
            original_rgb_plate = rgb_plate.copy()  # Keep original clean copy
            
            plt_size = (8, 8 * rgb_plate.shape[0] / rgb_plate.shape[1])
            fig, ax = plt.subplots(figsize=plt_size)
            plt.subplots_adjust(left=0.05, right=0.50, top=0.98, bottom=0.05)

            # Create permanent colorbar
            cmap = mpl.colormaps[cmap_c]
            norm = mpl.colors.Normalize(vmin=0, vmax=1)
            sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, shrink=0.4, location='right')
            cbar.set_ticks([0, 1])
            cbar.set_ticklabels(['Short Halo', 'Large Halo'], fontsize=5)
            

            ax_box = plt.axes([0.175, 0.075, 0.1, 0.05])
            text_box = TextBox(ax_box, 'Label: ', initial="")

            initial = [True, False, False, False]

            manager = plt.get_current_fig_manager()
            manager.window.state('zoomed')
            im = ax.imshow(rgb_plate)
            disabled_centers = [] # List of (x, y) tuples

            def is_disabled(current_center, disabled_list, tolerance=15):
                for dc in disabled_list:
                    # Euclidean distance check
                    dist = np.sqrt((current_center[0] - dc[0])**2 + (current_center[1] - dc[1])**2)
                    if dist < tolerance:
                        return True, dc
                return False, None
            
            def on_pick(event):
                patch = event.artist
                # Get the center of the patch we just clicked
                # (Assuming we stored the center in gid or it's accessible)
                click_center = patch.toxin_center 

                disabled, existing_center = is_disabled(click_center, disabled_centers)
                
                if disabled:
                    disabled_centers.remove(existing_center)
                else:
                    disabled_centers.append(click_center)

                update(None)

            def modular(epsilon_f=0.001, min_area_f=0.005, max_area_f=0.05, ratio_tolerance=(5/4), thresh_value=between_peaks, checks=initial):
                while ax.patches:
                    ax.patches[0].remove()
                black_peak, grey_peak, white_peak, grey_plate = find_peaks_in_plate(grey_image, plate, plate_radius)
                rgb_plate, contours = image_thresholding(black_peak, grey_peak, white_peak, grey_plate, thresh_value)
                blank_plate = rgb_plate.copy()
                original_rgb_plate = rgb_plate.copy() 
                
                all_toxin_vertices = []
                gaussian_blur = 71
                blurred_plate = cv.GaussianBlur(blank_plate, (gaussian_blur, gaussian_blur), 0)
                toxin_vertices, toxin_centres, polygon_areas = [], [], []
                target_colours = []
                masks = []
                
                # Always start with the original clean plate
                display_plate = original_rgb_plate.copy()
                
                for contour in contours:
                    toxin_vertices, centre, is_valid_contour, polygon_area = find_toxin_spot(contour, display_plate, all_toxin_vertices, toxin_centres, polygon_areas, epsilon_f, min_area_f, max_area_f, ratio_tolerance)

                    lawn_ring_vertices, deadzone_ring_vertices = [], []

                    if is_valid_contour:
                        for vertex in toxin_vertices:
                            lawn_ring_vertex, dead_ring_vertex = find_rings(vertex[0], centre[0], centre[1], plate_radius)
                            if lawn_ring_vertex is not None:
                                lawn_ring_vertices.append(lawn_ring_vertex)

                            deadzone_ring_vertices.append(dead_ring_vertex)
                        
                        # # Graphing
                        # import matplotlib.pyplot as plt
                        # blueberry_hex, blueberry_rgb = "#96AAFA", (150,170,250)
                        # cherry_hex, cherry_rgb = "#A03C6E", (160,60,110)
                        # honeydew_hex, honeydew_rgb = "#64d2be", (100, 210, 190)
                        # tomato_hex, tomato_rgb = "#F04650", (240,70,80)
                        # grape_hex, grape_rgb = "#7846C8", (120,70,200)

                        # plt.rcParams['font.family'] = 'sans-serif'
                        # plt.rcParams['font.sans-serif'] = 'Verdana'
                        # plt.rcParams["savefig.bbox"] = "tight"
                        # plt.rcParams["savefig.pad_inches"] = 0
                        # plt.rcParams["savefig.dpi"] = 600
                        # lawn_ring_polygon = np.array(lawn_ring_vertices, dtype=np.int32)
                        # deadzone_ring_polygon = np.array(deadzone_ring_vertices, dtype=np.int32)

                        # cv.drawContours(rgb_plate, [lawn_ring_polygon], -1, cherry_rgb, 5)
                        # cv.drawContours(rgb_plate, [deadzone_ring_polygon], -1, honeydew_rgb, 5)
                        # cv.circle(rgb_plate, (plate_radius,plate_radius), int((4/5)*plate_radius), blueberry_rgb, 5)
                        # plt.imshow(rgb_plate)
                        # plt.savefig("12_toxin_analysis.svg")
                        # plt.show()

                        outer_rings = np.array(lawn_ring_vertices, dtype=np.int32)
                        target_colour = get_target_colour(blank_plate,lawn_ring_vertices, deadzone_ring_vertices, checks[0])
                        target_colours.append(target_colour)

                #     outer_rings = np.array(lawn_ring_vertices, dtype=np.int32)
                #     print(outer_rings)
                #     masks.append(outer_rings)

                # print(len(masks))
                # circle_mask = np.zeros_like(grey_plate)
                # circle_mask_center = (plate[0], plate[1])
                # circle_mask_radius = plate_radius * (4/5)
                # cv.circle(circle_mask, circle_mask_center, int(circle_mask_radius), (255), thickness=-1)

                # cv.fillPoly(circle_mask, masks, 0)

                # result = cv.bitwise_and(blank_plate, blank_plate, mask=circle_mask)
                # cv.imshow("Masked Plate", result)
                # cv.waitKey(1)


                all_halo_distances, all_anorms, all_toxin_dirs, all_toxin_vers = [], [], [], []
                
                invalid_halos = 0

                from matplotlib.patches import Polygon
                for toxin_vertices, toxin_centre, polygon_area, target_colour in zip(all_toxin_vertices, toxin_centres, polygon_areas, target_colours):
                    poly_coords = toxin_vertices.reshape(-1, 2)

                    picker_radius = math.sqrt(polygon_area / math.pi)
                    print(picker_radius)
                    # Check if this specific spot is meant to be disabled
                    currently_disabled, _ = is_disabled(toxin_centre, disabled_centers)

                    poly = Polygon(np.array(toxin_vertices).reshape(-1, 2), 
                                closed=True, picker=5, zorder=10)
                    
                    # Attach the center to the artist so on_pick can find it
                    poly.toxin_center = toxin_centre 

                    if currently_disabled:
                        poly.set_facecolor('red')
                        poly.set_alpha(0.5)
                    else:
                        poly.set_facecolor('green')
                        poly.set_alpha(0.5)
                        
                    ax.add_patch(poly)

                    halo_distances, halo_directions, halo_vertices = [], [], []

                    for vertex in toxin_vertices:
                        get_halo_distance(toxin_centre, blurred_plate, vertex[0], target_colour, halo_distances, halo_directions, halo_vertices, line_length=200)

                    mean_halo, stdev_halo, lower_bound_halo, upper_bound_halo = statistics(halo_distances, 1)

                    valid_halos, valid_anorms, valid_dirs, valid_vers = [], [], [], []
                    
                    if not currently_disabled:
                            
                        for halo_index, halo_distance in enumerate(halo_distances):
                            allow_outliers = checks[1]
                            
                            halo_check, halo_d, halo_anorm, halo_dir, halo_ver = get_valid_halos(halo_distance, halo_index, mean_halo, stdev_halo, lower_bound_halo, upper_bound_halo, valid_halos, valid_anorms, valid_dirs, valid_vers, halo_directions, halo_vertices, allow_outliers, polygon_area, halo_distances)
                            


                            if halo_check is False:
                                invalid_halos += 1
                                # print(halo_d)
                    
                    all_halo_distances.append(valid_halos)
                    all_anorms.append(valid_anorms)
                    all_toxin_dirs.append(valid_dirs)
                    all_toxin_vers.append(valid_vers)

                
                a_norm = checks[2]
                if a_norm:
                    flat = [item for sublist in all_anorms for item in sublist]
                else:
                    flat = [item for sublist in all_halo_distances for item in sublist]                  

                flat_toxins = [item for sublist in all_toxin_vertices for item in sublist]
                # print(f"Found {len(flat)} valid halos, from {len(flat_toxins)} toxin spots, with {invalid_halos} invalid halos")
                
                if flat:
                    mean_halos, stdev_halos, lower_bound_halos, upper_bound_halos = statistics(flat, 1)
                    percent_cv = (stdev_halos/mean_halos) * 100
                    ax.set_title(f"{len(flat)} valid halos (μ={mean_halos:.3f}, σ={stdev_halos:.3f}, %CV={percent_cv:.3f})")
                else:
                    ax.set_title("No valid halos found")


                if not checks[3]:
                    cmap = mpl.colormaps[cmap_c]
                    all_valid_halos = [item for sublist in all_halo_distances for item in sublist]
                    all_valid_dirs = [item for sublist in all_toxin_dirs for item in sublist]
                    all_valid_vers = [item for sublist in all_toxin_vers for item in sublist]
                    colors = cmap(np.linspace(0, 1, len(all_valid_halos)))
                    # Convert matplotlib RGBA colors to OpenCV BGR format
                    colors_rgb = [(int(color[0]*255), int(color[1]*255), int(color[2]*255)) for color in colors]

                    sorted_indices = sorted(range(len(all_valid_halos)), key=lambda i: all_valid_halos[i])

                    for i, (valid_halo_distance, valid_halo_direction, valid_halo_vertex) in enumerate(zip(all_valid_halos, all_valid_dirs, all_valid_vers)):
                    
                        line_start = valid_halo_vertex
                        line_end_x = int(valid_halo_vertex[0] + (valid_halo_direction[0] * valid_halo_distance))
                        line_end_y = int(valid_halo_vertex[1] + (valid_halo_direction[1] * valid_halo_distance))
                        line_end = (line_end_x, line_end_y)

                        # Find where this halo ranks in the sorted order
                        color_index = sorted_indices.index(i)
                        cv.line(display_plate, line_start, line_end, colors_rgb[color_index], 2)

                # Update the image display
                im.set_array(display_plate)
                fig.canvas.draw()
                
                return all_halo_distances, display_plate

            # Run initial analysis
            all_halo_distances, _ = modular()
            fig.canvas.mpl_connect('pick_event', on_pick)
            epsilon_ax = plt.axes([0.60, 0.7, 0.3, 0.05])
            min_area_ax = plt.axes([0.60, 0.6, 0.3, 0.05])
            max_area_ax = plt.axes([0.60, 0.5, 0.3, 0.05])
            ratio_ax = plt.axes([0.60, 0.4, 0.3, 0.05])
            thresh_ax = plt.axes([0.60, 0.3, 0.3, 0.05])
            ax_check = plt.axes([0.60, 0.1, 0.3, 0.15])


            epsilon_slider = Slider(epsilon_ax, 'Epsilon', 2, 5, valinit=3, valstep=0.5, color = '#96aafa')
            min_area_slider = Slider(min_area_ax, 'Min Area', 0, 0.020, valinit=0.005, valstep=0.001, color = '#64d2be')
            max_area_slider = Slider(max_area_ax, 'Max Area', 0.020, 0.100, valinit=0.050, valstep=0.001, color = '#a03c6e')
            ratio_slider = Slider(ratio_ax, 'Ratio Tolerance', 1.0, 1.5, valinit=5/4, valstep=0.025, color = '#7846c8')
            thresh_slider = Slider(thresh_ax, 'Threshold', grey_peak, white_peak, valinit=between_peaks, valstep=2, color = '#f04650')

            labels = ['Ignore Speckle', 'Allow Outliers', 'Normalise to Area', 'Blank']
            checks = CheckButtons(ax_check, labels, initial)

            

            def update(val):
                
                updated_distances, new_plate = modular(
                    epsilon_f=10**(-epsilon_slider.val), 
                    min_area_f=min_area_slider.val, 
                    max_area_f=max_area_slider.val, 
                    ratio_tolerance=ratio_slider.val,
                    thresh_value=thresh_slider.val,
                    checks=checks.get_status()
                )
                # Update the global all_halo_distances for final processing
                nonlocal all_halo_distances
                all_halo_distances = updated_distances


            epsilon_slider.on_changed(update)
            min_area_slider.on_changed(update)
            max_area_slider.on_changed(update)
            ratio_slider.on_changed(update)
            thresh_slider.on_changed(update)
            checks.on_clicked(update)

            strain_names = []

            def submit(text):
                strain_names.append(text)
                # plt.close()
            
            text_box.on_submit(submit)

            plt.show()

            strain_name = strain_names[-1] if strain_names else "Unknown_Strain"

            short_file_name = os.path.basename(image_path)[:-4]
            image_file = Path(folder_name) / f"{short_file_name}_{strain_name}.svg"
            blank_image_file = Path(folder_name) / f"{short_file_name}_{strain_name}_blank.svg"

            # Get the final processed image with halos drawn
            _, final_processed_plate = modular(
                epsilon_f=10**(-epsilon_slider.val), 
                min_area_f=min_area_slider.val, 
                max_area_f=max_area_slider.val, 
                ratio_tolerance=ratio_slider.val,
                thresh_value=thresh_slider.val,
                checks=checks.get_status()
            )

            plt_size = (8, 8 * final_processed_plate.shape[0] / final_processed_plate.shape[1])
            plt.figure(figsize=plt_size)
            plt.imshow(final_processed_plate)
            plt.savefig(image_file, dpi=600)
            plt.close()

            plt_size = (8, 8 * blank_plate.shape[0] / blank_plate.shape[1])
            plt.figure(figsize=plt_size)
            plt.imshow(blank_plate)
            plt.savefig(blank_image_file, dpi=600)
            plt.close()

            # Process the final results after user interaction
            flat = [item for sublist in all_halo_distances for item in sublist]

            naming = f"{strain_name}_{short_file_name}"
            # naming = f"{p}_{os.path.basename(image_path)}"

            df = pd.read_excel(workbook_file, sheet_name='Sheet')
            df[f'{naming}'] = pd.Series(flat)

            with pd.ExcelWriter(workbook_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name='Sheet' ,index=False)
                
        except Exception as e:
            print(f"Error processing plate {p} in file {file}: {e} at line {e.__traceback__.tb_lineno}")
            continue

selected_folder = None

def select_folder():
    global selected_folder
    folder_path = filedialog.askdirectory()
    if folder_path:  # Only close if user selected a folder (didn't cancel)
        selected_folder = folder_path
        root.destroy()  # Close the app completely
        return folder_path

# Create main window
root = tk.Tk()
root.title("HaloUMI Home")
root.geometry("600x600")  # Adjust size as needed


import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# icon_path = resource_path("HaloUMI/HaloUMI_icon.ico")
icon_path = r"G:\My Drive\coding\HaloUMI\HaloUMI_icon.ico"
root.iconbitmap(icon_path)


# logo_path = resource_path("HaloUMI/HaloUMI_icon.png")
logo_path = r"G:\My Drive\coding\HaloUMI\HaloUMI_icon.png"
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((400, 400))  # Resize if needed
logo_photo = ImageTk.PhotoImage(logo_image)

root.logo_photo = logo_photo

logo_label = tk.Label(root, image=logo_photo)
logo_label.pack(pady=20)

# Create "Select Folder" button
select_button = tk.Button(root, text="Select Folder", command=select_folder, font=("Verdana", 14), bg="#96aafa", fg="white", padx=20, pady=10)
select_button.pack(pady=10)

# Run the app
root.mainloop()

folder_name = selected_folder

workbook = openpyxl.Workbook()
workbook_file = Path(folder_name) / "HaloUMI_output.xlsx"
workbook.save(workbook_file)

for i, file in enumerate(sorted(os.listdir(folder_name))):
    if file.endswith(".tif") or file.endswith(".tiff"):
        HaloUMI_main(folder_name, file)
# %%
