from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
NUM_CHANNELS = 3
IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
MAX_BRIGHTNESS = 255
STUFFS = ["Brightness", "Contrast", "RGB to Grayscale", "Flip", "Stacking", "Blurring"]



def get_img_list():
    """
    make a list of input items from folder INPUT
    :param directory:
    :return: list of input directory items as list of string
    """
    img_list = []
    with os.scandir() as i:
        for entry in i:
            if entry.is_file():
                if entry.name.lower().endswith(IMG_EXTENSIONS):
                    img_list.append(entry.name)

    return img_list


def menu(stuffs=None):
    stuffs = STUFFS if not stuffs else []
    menu_stuffs = dict(zip([i for i in range(len(stuffs))], stuffs))
    print("Index\t:\tStuff")
    for item in menu_stuffs.items():
        print("{}\t\t:\t{}".format(item[0], item[1]))


def adjust_brightness(img_mat: np.array, factor: int, adjustment="Increase"):
    if adjustment == "Increase":
        img_mat[img_mat + factor <= MAX_BRIGHTNESS] += factor
    else:
        img_mat[img_mat - factor >=0] -= factor
    return img_mat


def create_input(img, num_channels=NUM_CHANNELS):
    """
    Reshape 2d of vectors to 1d of vectors
    :param img:
    :return:
    """
    img_mat = np.array(img)
    input_mat = img_mat.reshape(img_mat.shape[0] * img_mat.shape[1], num_channels)
    return input_mat


if __name__ == "__main__":
    input_imgs = get_img_list()
    imgs_dict = dict(zip([i for i in range(len(input_imgs))],input_imgs))
    print(imgs_dict)
    selected = int(input("Select index of file to adjust: "))
    print("Selected: ", imgs_dict[selected])
    menu()
    factor = int(input("Enter factor that increase or decrease the brightness of image: "))
    msg = "Increase" if factor > 0 else "Decrease"
    new_factor = abs(factor)
    print(msg,"Brightness by", new_factor)
    with Image.open(imgs_dict[selected]) as img:
        mat = np.array(img)
        mat = adjust_brightness(mat, new_factor,adjustment=msg)
        plt.imshow(mat)
        plt.show()