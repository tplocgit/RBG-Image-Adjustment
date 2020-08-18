from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

NUM_CHANNELS = 3
IMG_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
MAX_BRIGHTNESS = 255
BRIGHTNESS = 0
CONTRAST = 1
GRAYSCALE = 2
FLIP = 3
STACKING = 4
BLURRING = 5
CHANGE_IMAGE = 6
EXIT = 7
STUFFS = ["Brightness", "Contrast", "Grayscale", "Flip", "Stacking", "Blurring", "Change image", "Exit"]


def is_image(entry):
    return entry.is_file() and entry.name.lower().endswith(IMG_EXTENSIONS) and entry.name


class MyImageEditor:
    """
    Contains functions that adjust image
    """

    def __init__(self, img_lst=None, tar=None, stuffs=None):
        self.images = img_lst if img_lst else []
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

    def show_target(self):
        """
        Show current image
        """
        plt.imshow(self.target)
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
        for i in range(self.target.shape[0]):
            for j in range(self.target.shape[1]):
                for k in range(self.target.shape[2]):
                    mul = int(self.target[i, j, k] * contrast_factor)
                    s = self.target[i, j, k] + brightness_factor
                    self.target[i, j, k] = mul if mul <= MAX_BRIGHTNESS else MAX_BRIGHTNESS
                    self.target[i, j, k] = s if s <= MAX_BRIGHTNESS else MAX_BRIGHTNESS
                    self.target[i, j, k] = s if s >= 0 else 0


if __name__ == "__main__":
    # Get list of image that can be adjusted
    editor = MyImageEditor(stuffs=STUFFS)
    editor.update_images()
    editor.list_images()
    selected = int(input("Select index of image in list that you want to adjust!\nYour choose: "))
    while selected not in range(len(editor.images)):
        selected = int(input("Invalid index please choose valid one in {}\nYour choose: "))
    editor.set_target(index=selected)
    selected = not EXIT
    while selected != EXIT:
        editor.show_menu()
        selected = int(input("Your choose: "))
        if selected == BRIGHTNESS:
            factor = int(input("Input factor to adjust brightness must be in range [-100:100] for best: "))
            editor.adjust_contrast_brightness(brightness_factor=factor)
            editor.show_target()
        else:
            print("This feature not available yet, please choose another feature")
