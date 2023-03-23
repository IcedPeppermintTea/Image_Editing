# Program that creates image patches from larger images
# Created it for my job at the Computational Vision Lab

# CHANGE MENU STYLE SO IT CAN PERFORM ALL OPERATIONS DURING ONE LOOP

import os
import cv2
from patchify import patchify
import tifffile as tiff
from PIL import Image

# Folder directories
initial_path = "original_img\\"
test = os.listdir(initial_path)  # create a list of all files and directories in specified path
resize_path = "resize_img\\"
patch_path = "patch_img\\"

# Introduction
print("Image Processing Program" + "\n")
resize = input("Do you wish to resize your images (y/n)? ")
cropping = input("Do you wish to crop your images (y/n)? ")
patches = input("Do you wish to create patches (y/n)?")

# Creating resize
if resize == 'y': # Resizing
    size_width = int(input("new size width: "))
    size_height = int(input("new size height: "))

    # Loop for every item in the folder
    # Learned this from https://stackoverflow.com/a/65585025
    for item in test:
        if item.endswith(".tif"):  # resize images that contain the .tif extension (one image)
            img = cv2.imread(initial_path + item, cv2.IMREAD_GRAYSCALE)  # make grayscale
            imgResize = cv2.resize(img, (size_width, size_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(resize_path + item[:-4] + '.tif', imgResize)
        elif item.endswith(".TIF"):  # resize images that contain the .TIF extension (the rest)
            img = cv2.imread(initial_path + item, cv2.IMREAD_GRAYSCALE)
            imgResize = cv2.resize(img, (size_width, size_height), interpolation=cv2.INTER_AREA)
            cv2.imwrite(resize_path + item[:-4] + '.TIF', imgResize)
        else:  # continue to next statement
            continue
    print("Resizing was completed successfully")

elif cropping == 'y':
    # what folder should be used depending on previous operations
    if resize == 'y': # use resized folder
        SOURCE_DIRECTORY = "resize_img"
    elif resize == 'n': # use original folder
        SOURCE_DIRECTORY = "original_img"
    else: # in case of error input, use original folder
        SOURCE_DIRECTORY = "original_img"

    crop_path = "crop_img/"
    directory_list = os.listdir(SOURCE_DIRECTORY)

# code mostly from https://stackoverflow.com/a/68775392
    for source_file in directory_list:
        source_path = os.path.join(SOURCE_DIRECTORY, source_file)
        if os.path.isfile(source_path):
            raw_image = Image.open(source_path)
            file_name = os.path.basename(source_path)
            file_name, extension = os.path.splitext(file_name)

            image_cropped_top = raw_image.crop((0, 0, 155, 256)) # (left, top, right, bottom)
            image_cropped_top.save(crop_path + file_name + 'TOP_Cropped.bmp', "BMP", quality=100)

    print("Cropping was completed successfully")

# Creating Patches
elif patches == 'y':
    # what folder should be used depending on previous operations
    if resize == 'y' and cropping == 'n': # use resized folder
        image_folder = tiff.imread("resize_img\\*.TIF")
    elif resize == 'n' and cropping == 'y': # use cropping folder
        image_folder = tiff.imread("crop_img\\*.TIF")
    elif resize == 'y' and cropping == 'y': # use cropping folder
        image_folder = tiff.imread("crop_img\\*.TIF")
    elif  resize == 'n' and cropping == 'n': # use original images
        image_folder = tiff.imread("original_img\\*.TIF")
    else: # in case of error input, use original folder
        image_folder = tiff.imread("original_img\\*.TIF")

    # Setting patch size and overlap
    patch_width = int(input("patch width: "))
    patch_height = int(input("patch height: "))
    want_overlap = input("Do you want overlap?")

    # Choosing overlap
    if want_overlap == 'n': # no overlap
        overlap = patch_width
    elif want_overlap == 'y': # yes to overlap
        overlap = int(input("Specify overlap: "))
    else:
        overlap = patch_width

    # code from a part of this youtube video https://youtu.be/7IL7LKSLb9I
    for img in range(image_folder.shape[0]):
        large_image = image_folder[img]
        patches_img = patchify(large_image, (patch_width, patch_height), step = overlap)

        for i in range(patches_img.shape[0]):
            for j in range(patches_img.shape[1]):
                single_patch_img = patches_img[i, j, :, :]  # rename for organization img_number_patchNumber
                # save into patches folder
                tiff.imwrite(patch_path + "image_" + str(img) + '_' + str(i) + str(j) + ".tif", single_patch_img)
    print("Patch extraction was completed successfully")
else:
    print("Error: Wrong input. Please try again")
    exit(1)



