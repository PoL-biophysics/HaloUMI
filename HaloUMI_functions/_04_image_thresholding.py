import numpy as np
import cv2 as cv
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

def image_thresholding(black_peak, grey_peak, white_peak, grey_plate, thresh_value):

    # between_peaks = (grey_peak + white_peak) // 2
    min_brightness = black_peak
    max_brightness = thresh_value

    brightness_range = max_brightness - min_brightness

    contrasted_plate = (((np.clip(grey_plate, min_brightness, max_brightness) - min_brightness) / brightness_range) * 255).astype(np.uint8)
    rgb_plate = cv.cvtColor(contrasted_plate, cv.COLOR_GRAY2RGB)

    _, thresholded_plate = cv.threshold(grey_plate, thresh_value, 255, cv.THRESH_BINARY)

    contours, _ = cv.findContours(thresholded_plate, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # # Graphing
    # contoured_plate = cv.drawContours(rgb_plate.copy(), contours, -1, grape_rgb, 3)
    # images = [contrasted_plate, thresholded_plate, contoured_plate]
    # image_names = ["08_contrasted-plate", "09_thresholded-plate", "10_contoured-plate"]
    # for i in range(len(images)):
    #     if i != 2:
    #         plt.imshow(images[i], cmap='gray')
    #         plt.savefig(f"{image_names[i]}.svg")
    #         plt.close()
    #     else:
    #         plt.imshow(images[i])
    #         plt.savefig(f"{image_names[i]}.svg")
    #         plt.close()

    return rgb_plate, contours