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

def preprocess_image(original_image_path,scale):

    original_image = cv.imread(original_image_path, cv.IMREAD_UNCHANGED)

    image_bit_depth = original_image.dtype
    # print(f"Image bit depth: {image_bit_depth}")
    # print(f"Original image shape: {original_image.shape}")
    # print(f"Original image dtype: {original_image.dtype}")
    if image_bit_depth == 'uint8':
        grey_image = original_image
    
    elif image_bit_depth == 'uint16':
        normalized_image = cv.normalize(original_image, None, 0, 65535, cv.NORM_MINMAX)
        grey_image = (original_image / 256).astype('uint8')

    # if bit depth is 32
    elif image_bit_depth == 'float32':
        normalized_image = cv.normalize(original_image, None, 0, 255, cv.NORM_MINMAX)
        grey_image = normalized_image.astype('uint8')


    contrasting_factor = 2
    contrasted_image = np.clip((grey_image.astype(np.float32) * contrasting_factor), 0, 255)
    contrasted_image = contrasted_image.astype('uint8')

    width = int(grey_image.shape[1] * scale)
    height = int(grey_image.shape[0] * scale)
    resized_image = cv.resize(contrasted_image, (width, height), interpolation = cv.INTER_AREA)

    # # Graphing
    # images = [original_image, grey_image, contrasted_image, resized_image]
    # image_names = ['01_original_image', '02_grey_image', '03_contrasted_image', '04_resized_image']
    # for i, img in enumerate(images):
    #     plt.imshow(img, cmap='gray')
    #     plt.savefig(f"{image_names[i]}.svg")
    #     plt.close()

    return grey_image, resized_image