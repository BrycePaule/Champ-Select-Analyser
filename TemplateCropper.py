import os
import Utils

import numpy as np
import cv2 as cv

from DRAFT_SLOTS import SLOT_COORDS
from PIL import Image


class TemplateCropper:

    def __init__(self):
        self.resize_factor = 0.01

        self.pick_width = None
        self.pick_height = None
        self.ban_width = None
        self.ban_height = None

        self.slot_coords = SLOT_COORDS

        self.check_slot_sizing()



    def crop_draft_slot(self, draft_filename, slot, iteration, bans=False):
        draft_image = Image.open(f'{Utils.path_draft_screenshots}{draft_filename}')
        draft_image = draft_image.crop(self.slot_coords[slot])

        width = self.ban_width if bans else self.pick_width
        height = self.ban_height if bans else self.pick_height

        if (iteration == 0):
            return cv.cvtColor(np.array(draft_image), cv.COLOR_RGB2GRAY)

        resize_down = iteration % 2 == 0

        # Alternates resizing up and down
        if iteration != 0 and resize_down:
            new_width = int(width - (width * self.resize_factor * iteration))
            new_height = int(height - (height * self.resize_factor * iteration))
            resized = True
        else:
            new_width = int(width + (width * self.resize_factor * iteration))
            new_height = int(height + (height * self.resize_factor * iteration))
            resized = True

        if (resized):
            draft_image = draft_image.resize((new_width, new_height))

        return cv.cvtColor(np.array(draft_image), cv.COLOR_RGB2GRAY) # COLOR_BGR2GRAY


    def check_slot_sizing(self):
        self.set_edge_lengths()

        bans = [slot for slot in self.slot_coords if len(slot) == 3]
        self.ensure_slots_consistent_size(bans, bans=True)

        picks = [slot for slot in self.slot_coords if len(slot) == 2]
        self.ensure_slots_consistent_size(picks)


    def ensure_slots_consistent_size(self, coord_list, bans=False):
        if bans:
            check_width = self.ban_width
            check_height = self.ban_height
        else:
            check_width = self.pick_width
            check_height = self.pick_height

        for slot in coord_list:
            x1, y1, x2, y2 = self.slot_coords[slot]
            width = x2 - x1
            height = y2 - y1

            if (width, height) != (check_width, check_height):
                raise Exception(f'Incorrect slot coordinates')


    def set_edge_lengths(self):
        x1, y1, x2, y2 = self.slot_coords['bb1']
        self.ban_width = x2 - x1
        self.ban_height = y2 - y1

        x1, y1, x2, y2 = self.slot_coords['b1']
        self.pick_width = x2 - x1
        self.pick_height = y2 - y1