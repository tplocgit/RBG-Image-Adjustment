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
STUFFS = ["Show", "Brightness", "Contrast", "Grayscale", "Flip", "Stacking", "Blurring", "Target", "Reset", "Exit"]
CONTRIBUTION = {"Red": 0.21, "Green": 0.72, "Blue": 0.11}
BOX_RANGE = range(-1, 2)


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
        self.images = img_lst if img_lst else []    # List of image that program can adjusts
        self.origin = tar                           # Origin image
        self.target = tar                           # Image selected
        self.can_do = stuffs                        # List of stuff that program can do

    def update_images(self) -> None:
        """
        Store all image's name in current folder
        """
        with os.scandir() as scanner:
            self.images = [entry.name for entry in scanner if is_image(entry)]

    def truncate(self):
        self.target[self.target > MAX_VALUE] = MAX_VALUE
        self.target[self.target < 0] = 0
        self.target = self.target.astype(int)

    def set_target(self, tar_index=None):
        """
        Set target to adjusting
        :param tar_index: Index of target in list of images
        """
        with Image.open(self.images[tar_index]) as img:
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
        Adjusts brightness and contrast of image.
        :param contrast_factor: Factor by which contrast of image increase or decrease.
        :param brightness_factor: Factor by which brightness of image increase or decrease.
        """
        self.target = (self.target - 128) * contrast_factor + 128 + brightness_factor
        self.truncate()

    def flip(self, lr=True):
        """
        Flip image in order left-right or up-down
        :param lr: Is flip left to right
        """
        self.target = np.fliplr(self.target) if lr else np.flipud(self.target)

    def gray_evaluation(self):
        """
        Evaluate gray colors of all pixel
        :return: Gray colors that evaluated
        """
        red = self.target[:, :, 0]
        green = self.target[:, :, 1]
        blue = self.target[:, :, 2]
        return red * CONTRIBUTION["Red"] + green * CONTRIBUTION["Green"] + blue * CONTRIBUTION["Blue"]

    def grayscale(self):
        """
        Convert RGB color to RBG grayscale
        """
        gray = self.gray_evaluation()
        for i in range(self.target.shape[2]):
            self.target[:, :, i] = gray
        self.target = self.target.astype(int)

    def stack(self, grayscale_img):
        """
        Stack 2 images together
        :param grayscale_img: grayscale-image with which target stack
        :return: Success or not
        """
        # Check size
        if self.target.shape != grayscale_img.shape:
            print("2 images not same size, please pick another image")
            return False
        # Grayscale self
        self.grayscale()
        # Stacking
        self.target = (self.target + grayscale_img) / 2
        self.truncate()
        return True

    def blurring(self):
        """
        Blur target image a little bit according to BOX BLUR algorithm
        """
        new_img = cp.deepcopy(self.target)
        for x in range(self.target.shape[0]):
            for y in range(self.target.shape[1]):
                # Check if out range
                if x < 1 or y < 1 or x + 1 >= self.target.shape[0] or y + 1 >= self.target.shape[1]:
                    continue

                s = np.zeros(3)  # Initial sum of pixels
                # Get pixel by pixel and add to s
                for dx in BOX_RANGE:
                    for dy in BOX_RANGE:
                        s = s + self.target[x + dx, y + dy]
                # Evaluate average
                new_img[x, y] = s * 1 / 9
        # Set to int element
        self.target = new_img.astype(int)


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
    editor.set_target(tar_index=selected)
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
            print("Input factor to adjust brightness must be in range [-100:100] for best: ", end="")
            factor = int(input())
            # Adjusting
            print("Adjusting ...")
            editor.adjust_contrast_brightness(brightness_factor=factor)
            print("Done. Check it out.")
            # Show result
            editor.show_img()
        elif selected == CONTRAST:
            # Input level
            print("Input level of contrast to adjust brightness must be in range [-255:255] to work properly: ", end="")
            level = int(input())
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
        elif selected == FLIP:
            print("Index\t|\tStuff")
            print("1\t\t|\tLeft to Right.")
            print("2\t\t|\tUp to Down.")
            print("Your choose: ")
            index = int_input()
            while index not in range(1, 3):
                print("Invalid index, please enter again: ")
                index = int_input()
            print("Flipping ...")
            editor.flip(lr=index == 1)
            print("Done. Check it out")
            editor.show_img()
        elif selected == GRAYSCALE:
            print("Converting ...")
            editor.grayscale()
            print("Done. Check it out.")
            editor.show_img()
        elif selected == CHANGE_IMAGE:
            editor.list_images()
            print("Select index of image in list that you want to adjust!\nYour choose: ", end="")
            selected = int_input()
            while selected not in range(len(editor.images)):
                print("Invalid index, please input again: ")
                selected = int_input()
            editor.set_target(tar_index=selected)
        elif selected == EXIT:
            print("Exiting ...")
            break
        elif selected == STACKING:
            new_editor = MyImageEditor()
            new_editor.update_images()
            new_editor.list_images()
            # Select image
            print("Select index of image in list that you want to stack with target!\nYour choose: ", end="")
            selected = int_input()
            while selected not in range(len(new_editor.images)):
                print("Invalid index, please input again: ")
                selected = int_input()
            new_editor.set_target(tar_index=selected)
            print("Stacking ...")
            new_editor.grayscale()
            is_stacked = editor.stack(new_editor.target)
            print("Done. Check it out.")
            if is_stacked:
                editor.show_img()
        elif selected == BLURRING:
            print("Blurring ...")
            editor.blurring()
            print("Done. Check it out.")
            editor.show_img()
        else:
            print("This feature not available yet, please choose another feature")

    print("Thanks for using!")
