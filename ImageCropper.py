import os

from pathlib import Path
from PIL import Image


class ImageCropper():


    def __init__(self):
        self.champlist_path = 'D:/Scripts/Python/Champ_Select_Analyser/champlist.txt'
        self.splash_path = 'D:/Scripts/Python/Champ_Select_Analyser/ChampSplashesFixed'
        self.icon_path = 'D:/Scripts/Python/Champ_Select_Analyser/ChampIconsFixed'
        self.champ_select_path = 'D:/Scripts/Python/Champ_Select_Analyser/ImageCropper/champ_selects/'

        self.template_path = 'D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/Templates/'
        self.results_path = 'D:/Scripts/Python/Champ_Select_Analyser/ImageMatcher/Results/'


    def clear_templates(self):
        """ Clears template directory of any previous templates """

        templates = [f for f in os.listdir(self.template_path) if f.endswith(".bmp")]

        for f in templates:
            os.remove(os.path.join(self.template_path, f))


    def get_crop_coordinates(self):
        """
         Generates lists of pick / ban coordinates.

         These are semi-manual, mostly follow the same pattern, but
         occasionally change break pattern to allow for accuracy, hence
         how this is written
         """

        bb1 = ("bb1", (40, 980, 110, 1050))
        bb2 = ("bb2", (130, 980, 200, 1050))
        bb3 = ("bb3", (220, 980, 290, 1050))
        bb4 = ("bb4", (315, 980, 385, 1050))
        bb5 = ("bb5", (408, 980, 478, 1050))
        rb1 = ("rb1", (1820, 980, 1890, 1050))
        rb2 = ("rb2", (1725, 980, 1795, 1050))
        rb3 = ("rb3", (1630, 980, 1700, 1050))
        rb4 = ("rb4", (1538, 980, 1608, 1050))
        rb5 = ("rb5", (1445, 980, 1515, 1050))
        ban_coords = [bb1, bb2, bb3, bb4, bb5, rb1, rb2, rb3, rb4, rb5]

        b1 = ("b1", (90, 180, 290, 320))
        b2 = ("b2", (90, 335, 290, 475))
        b3 = ("b3", (90, 495, 290, 635))
        b4 = ("b4", (90, 655, 290, 795))
        b5 = ("b5", (90, 810, 290, 950))
        r1 = ("r1", (1635, 180, 1835, 320))
        r2 = ("r2", (1635, 335, 1835, 475))
        r3 = ("r3", (1635, 495, 1835, 635))
        r4 = ("r4", (1635, 655, 1835, 795))
        r5 = ("r5", (1635, 810, 1835, 950))
        pick_coords = [b1, b2, b3, b4, b5, r1, r2, r3, r4, r5]

        return ban_coords, pick_coords


    def get_edge_sizes(self, list_of_coords):
        """ Returns the width and height of given selection of templates """

        self.check_edge_consistency(list_of_coords)

        a, b, c, d = list_of_coords[0]
        width = (c - a)
        height = (d - b)

        return width, height


    def check_edge_consistency(self, list_of_coords):
        """
        Runs through all templates coordinates, checking that they're of
        uniform size.

        If they're not all equal, raises exception
        """

        total_width = 0
        total_height = 0

        for index, (pick_slot, coords) in enumerate(list_of_coords):
            a, b, c, d = coords
            slot_width = (c - a)
            slot_height = (d - b)

            total_width += slot_width
            total_height += slot_height

            if total_width / index + 1 != slot_width:
                raise Exception(f'{pick_slot} is cropped differently than other coords')


    def crop_templates(self, champ_select_image, pick_coords, ban_coords, cropPath):

        for coords in pick_coords:
            cropped_image = champ_select_image.crop(coords[1])
            cropped_image.save(Path.joinpath(cropPath, coords[0] + ".bmp"))

        for coords in ban_coords:
            cropped_image = champ_select_image.crop(coords[1])
            cropped_image.save(Path.joinpath(cropPath, coords[0] + ".bmp"))


    def createResizedCopies(self, list_of_crops, number_of_copies, w, h, cropPath):

        for crop, coord in list_of_crops:

            crop_filename = crop + '.bmp'
            resize_factor_fixed = 0.01

            counter = -1
            resize_factor = resize_factor_fixed

            # create 'number_of_copies' smaller copies
            for i in range(number_of_copies):
                width = w
                height = h
                counter = str(int(counter) + 2).zfill(2)
                height = int(round(height - (height * resize_factor)))
                width = int(round(width - (width * resize_factor)))

                copy_image = Image.open(Path.joinpath(cropPath, str(crop_filename)))
                copy_image = copy_image.resize((width, height))
                copy_image.save(str(cropPath) + '/' + crop + '_' + str(counter) + '(s).bmp')

                resize_factor += resize_factor_fixed

            counter = 0
            resize_factor = resize_factor_fixed

            # create 'number_of_copies' bigger copies
            for i in range(number_of_copies):
                width = w
                height = h
                counter = str(int(counter) + 2).zfill(2)
                height = int(round(height + (height * resize_factor)))
                width = int(round(width + (width * resize_factor)))

                copy_image = Image.open(Path.joinpath(cropPath, str(crop_filename)))
                copy_image = copy_image.resize((width, height))
                copy_image.save(str(cropPath) + '/' + crop + '_' + str(counter) + '(b).bmp')

                resize_factor += resize_factor_fixed