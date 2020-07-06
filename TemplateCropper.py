import os

from PIL import Image


class TemplateCropper():


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


    """ TEMPLATE CREATION """

    def create_templates(self):
        """
        Main external function call.

        Uses all other methods to locate, create and save all template crops
        and duplicates
        """

        self.clear_stored_templates()

        self.check_crop_coordinates(self.ban_coords, bans=True)
        self.check_crop_coordinates(self.pick_coords)

        for champ_select in self.get_champ_select_image(all_templates=False):
            print('Cropper working on: ' + champ_select)

            image = Image.open(f'{self.champ_select_path}{champ_select}')

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

        if bans:
            width = self.ban_width
            height = self.ban_height
        else:
            width = self.pick_width
            height = self.pick_height

        for crop, coord in list_of_crops:
            crop_filename = crop + '.bmp'
            resize_factor_fixed = 0.01

            counter = -1
            resize_factor = resize_factor_fixed

            for i in range(self.duplicate_count):
                counter = str(int(counter) + 2).zfill(2)
                height = int(round(height - (height * resize_factor)))
                width = int(round(width - (width * resize_factor)))

                copy_image = Image.open(f'{self.template_path}{crop_filename}')
                copy_image = copy_image.resize((width, height))
                copy_image.save(f'{self.template_path}{crop}_{counter}(s).bmp')

                resize_factor += resize_factor_fixed

            counter = 0
            resize_factor = resize_factor_fixed

            for i in range(self.duplicate_count):
                counter = str(int(counter) + 2).zfill(2)
                height = int(round(height + (height * resize_factor)))
                width = int(round(width + (width * resize_factor)))

                copy_image = Image.open(f'{self.template_path}{crop_filename}')
                copy_image = copy_image.resize((width, height))
                copy_image.save(f'{self.template_path}{crop}_{counter}(b).bmp')

                resize_factor += resize_factor_fixed


    def get_champ_select_image(self, all_templates=False):
        """
        Returns the latest champ select screenshot, or a list of all
        screenshots in the directory if all=True
        """

        if all_templates:
            return (f for f in os.listdir(self.champ_select_path) if f.endswith(".bmp"))
        else:
            return [[f for f in os.listdir(self.champ_select_path) if f.endswith(".bmp")][-1]]


    """ SETUP """

    def clear_stored_templates(self):
        """ Clears template directory of any previous templates """

        templates = [f for f in os.listdir(self.template_path) if f.endswith(".bmp")]

        for f in templates:
            os.remove(os.path.join(self.template_path, f))


    """ CROP COORDINATES """

    @staticmethod
    def get_ban_coordinates():
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


    @staticmethod
    def get_pick_coordinates():
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


    def check_crop_coordinates(self, slot_coords_list, bans=False):
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


    @staticmethod
    def check_edge_size_consistency(slot_coords_list):
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