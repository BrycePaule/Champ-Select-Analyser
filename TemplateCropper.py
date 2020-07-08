import os
import sys

from PIL import Image


class TemplateCropper():

    """ Handles cutting template crops from champ select screenshots """

    def __init__(self, template_duplicate_count):
        self.champ_select_path = 'D:/Scripts/Python/ChampSelectAnalyser/ChampSelectScreenshots/'
        self.template_path = 'D:/Scripts/Python/ChampSelectAnalyser/Templates/'
        self.results_path = 'D:/Scripts/Python/ChampSelectAnalyser/Results/'

        self.pick_width = None
        self.pick_height = None
        self.ban_width = None
        self.ban_height = None

        self.pick_coords = self.get_pick_coordinates()
        self.ban_coords = self.get_ban_coordinates()

        self.duplicate_count = template_duplicate_count
        self.resize_factor = 0.01


    """ TEMPLATE CREATION """

    def create_templates(self, champ_select_image):
        """
        Main external function call.

        Uses all other methods to locate, create and save all template crops
        and duplicates
        """

        self.clear_stored_templates()

        self.get_crop_coordinates(self.ban_coords, bans=True)
        self.get_crop_coordinates(self.pick_coords)

        print('Cropper working on: ' + champ_select_image)

        image = Image.open(f'{self.champ_select_path}{champ_select_image}')

        print('                                ... cropping templates')
        self.crop_templates(image, self.ban_coords)
        self.crop_templates(image, self.pick_coords)

        print('                                ... making duplicates')
        self.create_duplicates(self.ban_coords, bans=True)
        self.create_duplicates(self.pick_coords)


    def crop_templates(self, champ_select_image, coordinates):
        """ Crops and saves templates from the given coordinates """

        for coords in coordinates:
            cropped_image = champ_select_image.crop(coords[1])
            cropped_image.save(f'{self.template_path}{coords[0]}.bmp')


    def create_duplicates(self, list_of_crops, bans=False):
        """
        Creates template duplates resized in self.resize_factor increments.

        Allows for an extra layer of safety, if the champion splash / icon
        is not perfectly sized, will attempt to match the duplicates before
        moving on
        """

        if bans:
            width = self.ban_width
            height = self.ban_height
        else:
            width = self.pick_width
            height = self.pick_height

        for label, _ in list_of_crops:
            template = Image.open(f'{self.template_path}{label}.bmp')

            for i in range(1, self.duplicate_count + 1):
                sml_width = int(width - (width * ((i + 1) * self.resize_factor)))
                sml_height = int(height - (height * ((i + 1) * self.resize_factor)))
                sml_index = str((i * 2) - 1).zfill(2)
                sml_template = template.resize((sml_width, sml_height))
                sml_template.save(f'{self.template_path}{label}_{sml_index}.bmp')

                lrg_width = int(width + (width * ((i + 1) * self.resize_factor)))
                lrg_height = int(height + (height * ((i + 1) * self.resize_factor)))
                lrg_index = str(i * 2).zfill(2)
                lrg_template = template.resize((lrg_width, lrg_height))
                lrg_template.save(f'{self.template_path}{label}_{lrg_index}.bmp')

    """ SETUP """

    def clear_stored_templates(self):
        """ Clears template directory of any previous templates """

        templates = [f for f in os.listdir(self.template_path) if f.endswith(".bmp")]

        for f in templates:
            os.remove(os.path.join(self.template_path, f))


    """ CROP COORDINATES """

    def get_ban_coordinates(self):
        """
         Generates lists of ban coordinates.

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

        return [bb1, bb2, bb3, bb4, bb5, rb1, rb2, rb3, rb4, rb5]


    def get_pick_coordinates(self):
        """
         Generates lists of pick coordinates.

         These are semi-manual, mostly follow the same pattern, but
         occasionally change break pattern to allow for accuracy, hence
         how this is written
         """

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

        return [b1, b2, b3, b4, b5, r1, r2, r3, r4, r5]


    def get_crop_coordinates(self, slot_coords_list, bans=False):
        """ Returns the width and height of given selection of templates """

        self.check_edge_size_consistency(slot_coords_list)

        a, b, c, d = slot_coords_list[0][1]
        width = (c - a)
        height = (d - b)

        if bans:
            self.ban_width = width
            self.ban_height = height
        else:
            self.pick_width = width
            self.pick_height = height


    def check_edge_size_consistency(self, slot_coords_list):
        """
        Runs through all templates coordinates, checking that they're of
        uniform size.

        If they're not all equal, raises exception
        """

        total_width = 0
        total_height = 0

        for index, (pick_slot, slot_coords_list) in enumerate(slot_coords_list):
            a, b, c, d = slot_coords_list
            slot_width = (c - a)
            slot_height = (d - b)

            total_width += slot_width
            total_height += slot_height

            if total_width / (index + 1) != slot_width:
                raise Exception(f'{pick_slot} is cropped differently than other coords')