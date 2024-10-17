import os
import Utils

from PIL import Image
import numpy as np
import cv2 as cv


class TemplateCropper:

    """ Handles cutting template crops from champ select screenshots """

    def __init__(self, template_duplicate_count):
        self.duplicate_count = template_duplicate_count
        self.resize_factor = 0.01

        self.pick_width = None
        self.pick_height = None
        self.ban_width = None
        self.ban_height = None

        self.slot_coords = self.build_slot_coords()

    """ TEMPLATE CREATION """

    def create_template(self, champ_select_image, slot, template_number, resize_factor=0.01, bans=False):
        template_PIL = Image.open(f'{Utils.path_champlist}{champ_select_image}')
        template_PIL = template_PIL.crop(self.slot_coords[slot])

        if template_number == 0:
            return cv.cvtColor(np.array(template_PIL), cv.COLOR_RGB2GRAY)

        width = self.ban_width if bans else self.pick_width
        height = self.ban_height if bans else self.pick_height

        if template_number % 2 == 0:
            new_width = int(width - (width * resize_factor * template_number))
            new_height = int(height - (height * resize_factor * template_number))
        else:
            new_width = int(width + (width * resize_factor * template_number))
            new_height = int(height + (height * resize_factor * template_number))

        template_PIL = template_PIL.resize((new_width, new_height))
        template_CV = cv.cvtColor(np.array(template_PIL), cv.COLOR_BGR2GRAY)

        return template_CV


    """ CROP COORDINATES """

    def build_slot_coords(self):
        coords = {
            # bans
            'bb1': (40, 980, 110, 1050),
            'bb2': (130, 980, 200, 1050),
            'bb3': (220, 980, 290, 1050),
            'bb4': (315, 980, 385, 1050),
            'bb5': (408, 980, 478, 1050),
            'rb1': (1820, 980, 1890, 1050),
            'rb2': (1725, 980, 1795, 1050),
            'rb3': (1630, 980, 1700, 1050),
            'rb4': (1538, 980, 1608, 1050),
            'rb5': (1445, 980, 1515, 1050),

            # picks
            'b1': (90, 180, 290, 320),
            'b2': (90, 335, 290, 475),
            'b3': (90, 495, 290, 635),
            'b4': (90, 655, 290, 795),
            'b5': (90, 810, 290, 950),
            'r1': (1635, 180, 1835, 320),
            'r2': (1635, 335, 1835, 475),
            'r3': (1635, 495, 1835, 635),
            'r4': (1635, 655, 1835, 795),
            'r5': (1635, 810, 1835, 950)
        }

        self.check_size_consistency(list(coords.values())[:10])
        self.check_size_consistency(list(coords.values())[10:])
        self.get_crop_measurements(coords)

        return coords

    def check_size_consistency(self, coord_list):
        """
        Runs through all templates coordinates, checking that they're of
        uniform size.

        If they're not all equal, raises exception
        """

        template_width = coord_list
        template_height = 0

        for slot in coord_list[1:]:
            x1, y1, x2, y2 = slot

            if template_width == 0 or template_height == 0:
                template_width = x2 - x1
                template_height = y2 - y1
                continue

            if x2 - x1 != template_width or y2 - y1 != template_height:
                raise Exception(f'Incorrect cropper slot coordinates')

    def get_crop_measurements(self, slot_coords):
        """ Returns the width and height of given selection of templates """

        x1, y1, x2, y2 = slot_coords['bb1']
        self.ban_width = x2 - x1
        self.ban_height = y2 - y1

        x1, y1, x2, y2 = slot_coords['b1']
        self.pick_width = x2 - x1
        self.pick_height = y2 - y1