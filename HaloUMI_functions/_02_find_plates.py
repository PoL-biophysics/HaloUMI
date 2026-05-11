import cv2 as cv
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

def find_plates(resized_image, scale):
    
    plates = cv.HoughCircles(
        resized_image,
        method=cv.HOUGH_GRADIENT,
        dp= 1,
        minDist= int(2000 * scale),
        param1= 50,
        param2= 30,
        minRadius= int(900 * scale),
        maxRadius= int(1100 * scale)
    )

    plates = np.uint16(np.around(plates))

    # #Graphing
    # rgb_plates = cv.cvtColor(resized_image, cv.COLOR_GRAY2RGB)
    # for plate in plates[0, :]:
    #     center = (plate[0], plate[1])
    #     radius = plate[2]
    #     cv.circle(rgb_plates, center, radius, tomato_rgb, 2)
    #     cv.circle(rgb_plates, center, 10, honeydew_rgb, -1)

    
    # plt.imshow(rgb_plates)
    # plt.savefig("05_detected-plates.svg")
    # plt.close() 

    plates[0, :, :3] = (plates[0, :, :3].astype(float) / scale).astype(np.uint16)

    plate_centers = [(plate[0], plate[1]) for plate in plates[0, :]]

   

    return plates