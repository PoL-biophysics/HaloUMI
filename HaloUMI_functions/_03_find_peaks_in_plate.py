import cv2 as cv
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

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

def find_peaks_in_plate(grey_image, plate, plate_radius):

    x, y = plate[0], plate[1]
    top_left_x = max(0, x - plate_radius)
    top_left_y = max(0, y - plate_radius)
    bottom_right_x = min(grey_image.shape[1], x + plate_radius)
    bottom_right_y = min(grey_image.shape[0], y + plate_radius)

    grey_plate = grey_image[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

    # plt.imshow(grey_plate, cmap='gray')
    # plt.show()

    grey_plate_hist = cv.calcHist([grey_plate], [0], None, [256], [0, 256]).flatten()
    grey_plate_smooth_hist = gaussian_filter1d(grey_plate_hist, sigma=3)

    # # Graphing
    # plt.hist(grey_plate.flatten(), bins=256, color=blueberry_hex, alpha=0.5, label='Grey Plate Intensity Frequency')
    # plt.plot(grey_plate_smooth_hist, color=grape_hex, label='Smoothed Peaks')
    # plt.xlabel('Pixel Intensity')
    # plt.ylabel('Frequency')
    # plt.legend()
    # plt.gca().spines['top'].set_visible(False)
    # plt.gca().spines['right'].set_visible(False)
    # plt.savefig("06_grey_plate_histogram.svg")
    # plt.close()


    peaks, proms = find_peaks(grey_plate_smooth_hist, prominence=50)

    big_peaks = []
    for peak in peaks:
        if grey_plate_smooth_hist[peak] > 50000:
            big_peaks.append(peak)
    
    if len(big_peaks) > 1:
        grey_peak = big_peaks[-1]
        black_peak = 0
    else:
        grey_peak = big_peaks[0]
        black_peak = 0

    import numpy as np
    first_derivative = np.gradient(grey_plate_smooth_hist)
    seccond_derivative = np.gradient(first_derivative)

    local_minima, _ = find_peaks(-seccond_derivative, prominence=20)

    white_peak = None
    for minima in local_minima:
        if minima > grey_peak and grey_plate_smooth_hist[minima] < grey_plate_smooth_hist[grey_peak]*0.1:
            # local minima must be lower than 10
            if seccond_derivative[minima] < -20:
                white_peak = minima
                break

    if white_peak is None:
        #set white peak to point at  which plot crosses 5000 after grey peak
        for i in range(grey_peak, len(grey_plate_smooth_hist)):
            if grey_plate_smooth_hist[i] < 5000:
                white_peak = i
                break
            else:
                white_peak = grey_peak+10
    

    # plt.figure(figsize=(10, 6))
    # plt.plot(grey_plate_smooth_hist, label='Smoothed Histogram', color='gray')
    # plt.plot(first_derivative, label='First Derivative', color='blue')
    # plt.plot(seccond_derivative, label='Second Derivative', color='green')
    # plt.plot(local_minima, grey_plate_smooth_hist[local_minima], "s", label='Local Minima', color='crimson')

    # # Mark all detected peaks
    # plt.plot(peaks, grey_plate_smooth_hist[peaks], "x", label='Detected Peaks', color='blue')

    # # Highlight big peaks
    # plt.plot(big_peaks, grey_plate_smooth_hist[big_peaks], "o", label='Big Peaks', color='red')

    # # Annotate key peaks
    # plt.axvline(x=black_peak, color='black', linestyle='--', label='Black Peak')
    # plt.axvline(x=grey_peak, color='green', linestyle='--', label='Grey Peak')
    # plt.axvline(x=white_peak, color='orange', linestyle='--', label='White Peak')

    # plt.title("Smoothed Intensity Histogram of Plate Region")
    # plt.xlabel("Pixel Intensity")
    # plt.ylabel("Frequency")
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.savefig("07_peak_detection_details.svg")
    # plt.close()


    return black_peak, grey_peak, white_peak, grey_plate