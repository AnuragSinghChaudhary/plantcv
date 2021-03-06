# Pseudocolor any grayscale image

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error


def pseudocolor(gray_img, mask=None, cmap=None, background="image", min_value=0, max_value=255, obj=None, dpi=None,
                axes=True, path="."):
    """Pseudocolor any grayscale image to custom colormap

    Inputs:
    gray_img    = grayscale image data
    mask        = binary mask
    cmap        = colormap
    background  = background color/type. Options are "image" (gray_img), "white", or "black".
                  A mask must be supplied
    min_value   = minimum value for range of interest
    max_value   = maximum value for range of interest
    obj         = if provided, the pseudocolored image gets cropped down to the region of interest
    dpi         = dots per inch
    axes        = if False then x- and y-axis won't be displayed
    path        = path for location for saving the image

    Returns:
    pseudo_image = pseudocolored image

    :param gray_img: numpy.ndarray
    :param mask: numpy.ndarray
    :param cmap: str
    :param background: str
    :param min_value: int
    :param max_value: int
    :param obj: numpy.ndarray
    :param dpi: int
    :param axes: bool
    :param path: str
    :return pseudo_image: numpy.ndarray
    """

    # Auto-increment the device counter
    params.device += 1

    # Check if the image is grayscale
    if len(np.shape(gray_img)) != 2:
        fatal_error("Image must be grayscale.")
    if max != 255:
        # Any pixels above the max_value set to the max value
        gray_img[gray_img > max_value] = max_value
    if min_value != 0:
        # Any pixels below min_value set to the min_value value
        gray_img[gray_img < min_value] = min_value

    # Apply the mask if given
    if mask is not None:
        if obj is not None:
            # Copy the image
            img_copy = np.copy(gray_img)
            # Extract contour size
            x, y, w, h = cv2.boundingRect(obj)
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 5)

            # Crop down the image
            crop_img = gray_img[y:y + h, x:x + w]

            # Calculate the buffer size based on the contour size
            offsetx = int(w / 5)
            offsety = int(h / 5)

            # Crop img including buffer
            gray_img = cv2.copyMakeBorder(crop_img, offsety, offsety, offsetx, offsetx, cv2.BORDER_CONSTANT,
                                          value=(0, 0, 0))

            # Crop the mask to the same size
            crop_mask = mask[y:y + h, x:x + w]
            mask = cv2.copyMakeBorder(crop_mask, offsety, offsety, offsetx, offsetx, cv2.BORDER_CONSTANT,
                                      value=(0, 0, 0))

        # Apply the mask
        masked_img = np.ma.array(gray_img, mask=~mask.astype(np.bool))

        # Set the background color or type
        if background == "black":
            # Background is all zeros
            bkg_img = np.zeros(np.shape(gray_img), dtype=np.uint8)
            # Use the gray cmap for the background
            bkg_cmap = "gray"
        elif background == "white":
            # Background is all 255 (white)
            bkg_img = np.zeros(np.shape(gray_img), dtype=np.uint8)
            bkg_img += 255
            # Use the reverse gray cmap for the background
            bkg_cmap = "gray_r"
        elif background == "image":
            # Set the background to the inpute gray image
            bkg_img = gray_img
            # Use the gray cmap for the background
            bkg_cmap = "gray"
        else:
            fatal_error(
                "Background type {0} is not supported. Please use 'white', 'black', or 'image'.".format(background))

        # Pseudocolor the image
        # Plot the background first
        pseudo_img1 = plt.imshow(bkg_img, cmap=bkg_cmap)
        # Overlay the masked grayscale image with the user input colormap
        plt.imshow(masked_img, cmap=cmap)

        # Include image title
        plt.title('Pseudocolored image')  # + os.path.splitext(filename)[0])

        # Include the colorbar
        plt.colorbar(fraction=0.033, pad=0.04)

        # Remove axes
        if axes is False:
            plt.xticks([])
            plt.yticks([])

        pseudo_img = plt.gcf()

        # Print or plot if debug is turned on
        if params.debug == 'print':
            plt.savefig(os.path.join(path, str(params.device) + '_pseudocolored.png'), dpi=dpi)
        elif params.debug == 'plot':
            plot_image(pseudo_img1)
    else:
        # Pseudocolor the image
        pseudo_img1 = plt.imshow(gray_img, cmap=cmap)

        # Include image title
        plt.title('Pseudocolored image')  # + os.path.splitext(filename)[0])

        # Include the colorbar
        plt.colorbar(fraction=0.033, pad=0.04)

        # Remove axes
        if axes is False:
            plt.xticks([])
            plt.yticks([])

        pseudo_img = plt.gcf()

        # Print or plot if debug is turned on
        if params.debug == 'print':
            plt.savefig(os.path.join(path, str(params.device) + '_pseudocolored.png'), dpi=dpi)
        elif params.debug == 'plot':
            plot_image(pseudo_img1)

    return pseudo_img
