# Program that creates image patches from larger images
# Created it for my job at the Computational Vision Lab
# Ayleen Roque
# Year: 2021 - 2022
# Note: Most of the code here is recycled from other programs on the web, which helped me learn image processing a lot

# Libraries
import os
import cv2
from patchify import patchify
import tifffile as tiff
from PIL import Image

# Folder directories (for reference)
initial_path = "original_img\\"
test = os.listdir(initial_path)  # create a list of all files and directories in specified path
resize_path = "resize_img\\"
patch_path = "patch_img\\"

# Password log in prototype
password = input("Enter Password: ")
if (password == "comp_vis123"):
    # Introduction
    print("Image Processing Program" + "\n")

    # Menu Options
    print("Choose one of the following options:\n")
    print("1. Resize images \n"
          "2. Crop images \n"
          "3. Extract image patches\n")
    choice = int(input("Enter choice here: "))

    # Menu loop
    if choice == 1:
        # resize
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

    elif choice == 2:
        # crop

        # If we should use resized images or original images
        yes = input("Use resized images?(y/n): ")
        if yes == 'y':
            SOURCE_DIRECTORY = resize_path
        else:
            SOURCE_DIRECTORY = initial_path

        crop_path = "crop_img/"  # adding / for specifying inside the folder
        directory_list = os.listdir(SOURCE_DIRECTORY)

        # code mostly from https://stackoverflow.com/a/68775392
        for source_file in directory_list:
            source_path = os.path.join(SOURCE_DIRECTORY, source_file)
            if os.path.isfile(source_path):
                raw_image = Image.open(source_path)
                file_name = os.path.basename(source_path)
                file_name, extension = os.path.splitext(file_name)

                image_cropped_top = raw_image.crop((0, 0, 155, 256))  # (left, top, right, bottom)
                image_cropped_top.save(crop_path + file_name + 'TOP_Cropped.bmp', "BMP", quality=100)

        print("Cropping was completed successfully")
    elif choice == 3:
        # patch

        # What folder we should use
        yes = input("What folder should we use?(r/c/o): ")

        # specifying the file type
        # using .TIF for better quality
        if yes == 'r':
            image_folder = tiff.imread("resize_img\\*.TIF")
        elif yes == 'c':
            image_folder = tiff.imread("crop_img\\*.TIF")
        else:
            image_folder = tiff.imread("original_img\\*.TIF")

        # Setting patch size and overlap
        patch_width = int(input("patch width: "))
        patch_height = int(input("patch height: "))
        want_overlap = input("Do you want overlap?")

        # Choosing overlap
        if want_overlap == 'n':  # no overlap
            overlap = patch_width
        elif want_overlap == 'y':  # yes to overlap
            overlap = int(input("Specify overlap: "))
        else:
            overlap = patch_width

        # code from a part of this youtube video https://youtu.be/7IL7LKSLb9I
        for img in range(image_folder.shape[0]):
            large_image = image_folder[img]
            patches_img = patchify(large_image, (patch_width, patch_height), step=overlap)

            for i in range(patches_img.shape[0]):
                for j in range(patches_img.shape[1]):
                    single_patch_img = patches_img[i, j, :, :]  # rename for organization img_number_patchNumber
                    # save into patches folder
                    tiff.imwrite(patch_path + "image_" + str(img) + '_' + str(i) + str(j) + ".tif", single_patch_img)
        print("Patch extraction was completed successfully")
    else:
        # if user inputs choice outside of range
        # exit safely
        print("Error. Please try again")
        exit(1)
else:
    print("Wrong password. Please speak to employee for further instructions")
    exit(2)
