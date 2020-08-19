from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import copy as cp

IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
MAX_VALUE = 255
SHOW = 0
BRIGHTNESS = SHOW + 1
CONTRAST = BRIGHTNESS + 1
GRAYSCALE = CONTRAST + 1
FLIP = GRAYSCALE + 1
STACKING = FLIP + 1
BLURRING = STACKING + 1
CHANGE_IMAGE = BLURRING + 1
RESET = CHANGE_IMAGE + 1
EXIT = RESET + 1
STUFFS = ["Show", "Brightness", "Contrast", "Grayscale", "Flip", "Stacking", "Blurring", "Change image", "Reset", "Exit"]



def is_image(entry):
    return entry.is_file() and entry.name.lower().endswith(IMG_EXTENSIONS) and entry.name


def contrast_factor_evaluation(contrast):
    return (259 * (contrast + 255)) / (255 * (259 - contrast))


def int_input():
    num = input()
    while not num.isnumeric():
        num = input("Invalid input, please input again: ")
    return int(num)


class MyImageEditor:
    """
    Contains functions that adjust image
    """

    def __init__(self, img_lst=None, tar=None, stuffs=None):
        self.images = img_lst if img_lst else []
        self.origin = tar
        self.target = tar
        self.can_do = stuffs

    def update_images(self) -> None:
        """
        Store all image's name in current folder
        """
        with os.scandir() as scanner:
            self.images = [entry.name for entry in scanner if is_image(entry)]

    def set_target(self, index=None):
        """
        Set target to adjusting
        :param index: Index of target in list of images
        """
        with Image.open(self.images[index]) as img:
            self.target = np.array(img)
            self.target = self.target.astype(int)
            self.origin = cp.deepcopy(self.target)

    def reset(self):
        self.target = cp.deepcopy(self.origin)

    def show_img(self, img=None):
        """
        Show current image
        """
        img = img if img else self.target
        plt.imshow(img)
        plt.show()

    def list_images(self):
        print("Index\t|\tImage")
        for i in range(len(self.images)):
            print("\t{}\t|\t{}".format(i, self.images[i]))

    def show_menu(self) -> None:
        """
        Print stuffs that program can do like Index | Stuff.
        :return: None.
        """
        menu_stuffs = dict(zip([i for i in range(len(self.can_do))], self.can_do)) if self.can_do else []
        if menu_stuffs:
            print("Index\t:\tStuff")
            for item in menu_stuffs.items():
                print("{}\t\t:\t{}".format(item[0], item[1]))
        else:
            print("MAINTENANCES")

    def adjust_contrast_brightness(self, brightness_factor=0, contrast_factor=1.0) -> None:
        """
        Adjusts brightness of image.
        :param contrast_factor:
        :param brightness_factor: Factor by which image increase or decrease.
        :param brightness_factor:
        """
        self.target = (self.target - 128) * contrast_factor + 128 + brightness_factor
        self.target[self.target > MAX_VALUE] = MAX_VALUE
        self.target[self.target < 0] = 0
        self.target = self.target.astype(int)


if __name__ == "__main__":
    # Get list of image that can be adjusted
    editor = MyImageEditor(stuffs=STUFFS)
    editor.update_images()
    editor.list_images()
    # Select image
    print("Select index of image in list that you want to adjust!\nYour choose: ", end="")
    selected = int_input()
    while selected not in range(len(editor.images)):
        print("Invalid index, please input again: ")
        selected = int_input()
    editor.set_target(index=selected)
    # Program main stuff started
    selected = not EXIT
    while selected != EXIT:
        # Show menu
        editor.show_menu()
        # Choose stuff
        selected = input("Your choose: ")
        while not selected.isnumeric():
            selected = input("Invalid input, please input again: ")
        selected = int(selected)
        # Do stuff
        if selected == BRIGHTNESS:
            # Input factor
            factor = input("Input factor to adjust brightness must be in range [-100:100] for best: ")
            while not factor.isnumeric():
                factor = input("Invalid input, please input again: ")
            factor = int(factor)
            # Adjusting
            print("Adjusting ...")
            editor.adjust_contrast_brightness(brightness_factor=factor)
            print("Done. Check it out.")
            # Show result
            editor.show_img()
        elif selected == CONTRAST:
            # Input level
            print("Input level of contrast to adjust brightness must be in range [-255:255] to work properly: ", end="")
            level = int_input()
            # Evaluate factor
            factor = contrast_factor_evaluation(level)
            print("Factor is:", factor)
            # Adjusting
            print("Adjusting ...")
            editor.adjust_contrast_brightness(contrast_factor=factor)
            # Show
            print("Done. Check it out.")
            editor.show_img()
        elif selected == SHOW:
            print("Showing target image")
            editor.show_img()
            print("Done.")
        elif selected == RESET:
            print("Resetting ...")
            editor.reset()
            print("Done. Check it out.")
            editor.show_img()
        else:
            print("This feature not available yet, please choose another feature")
