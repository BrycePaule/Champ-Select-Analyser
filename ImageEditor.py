import os
import Utils

from PIL import Image, ImageOps, ImageChops, ImageDraw, ImageEnhance

from IMAGE_TRANSFORMATIONS import IMAGE_TRANSFORMATIONS


class ImageEditor:

    """
    Contains all methods to correct differences between broadcast graphics
    and default splash arts / icons.

    Includes cropping, tilting, enhancing, darkening, covering unwanted champ
    portraits, mirroring, etc.

    """

    def __init__(self):
        self.champlist = Utils.read_champlist_from_file()

        self.check_missing_champions()


    """ IMAGE EDITING """

    def optimise_splashes(self, champ_name):
        splash = Image.open(f'{Utils.path_splashes_raw}{champ_name}.bmp')

        splash = self.splash_blockout_secondaries(champ_name, splash)
        splash = self.splash_manual_overrides(champ_name, splash)
        splash = self.splash_crop(champ_name, splash)
        splash = self.splash_resize(champ_name, splash)

        splash.save(f'{Utils.path_splashes}{champ_name}.bmp')
        splash = ImageOps.mirror(splash)
        splash.save(f'{Utils.path_splashes}{champ_name}_inverted.bmp')


    def optimise_icons(self, champ_name):
        icon = Image.open(f'{Utils.path_icons_raw}{champ_name}.bmp')

        icon = self.icon_manual_override(champ_name, icon)
        icon = self.icon_resize(champ_name, icon)

        icon.save(f'{Utils.path_icons}{champ_name}.bmp')
        icon = ImageOps.mirror(icon)
        icon.save(f'{Utils.path_icons}{champ_name}_inverted.bmp')


    def splash_resize(self, champ_name, splash):
        if champ_name not in IMAGE_TRANSFORMATIONS:
            return splash

        scale_factor = IMAGE_TRANSFORMATIONS[champ_name].splash_scale

        if scale_factor == 1.00:
            return splash

        Utils.print_indented(' - scaling splash')

        w, h = splash.size
        w = round(w * scale_factor)
        h = round(h * scale_factor)
        splash = splash.resize((w, h))

        return splash


    def splash_blockout_secondaries(self, champ_name, splash):
        #  Blocks out unwanted champions from dual champion splashes. 

        if champ_name == 'Xayah':
            Utils.print_indented(' - blocking out Rakan')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(400, 20), (600, 200)], 'black')

        elif champ_name == 'Rakan':
            Utils.print_indented(' - blocking out Xayah')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(300, 120), (500, 300)], 'black')

        elif champ_name == 'Kayle':
            Utils.print_indented(' - blocking out Morgana')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(200, 120), (500, 300)], 'black')

        elif champ_name == 'Morgana':
            Utils.print_indented(' - blocking out Kayle')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(200, 120), (500, 300)], 'black')

        return splash


    def splash_manual_overrides(self, champ_name, splash):
        """
        Crops and edits each splash to be recognisable by its crop.

        Some splashes get rotated / edited by broadcast graphic teams for
        aesthetics, this converts the raw splash arts to a much closer
        form that's used on broadcast to be able to match.
        """

        # Manual overrides, rotations and misc transformations
        if champ_name == 'Camille':
            Utils.print_indented(' - tilting')
            splash = splash.rotate(2)

        elif champ_name == 'Corki':
            Utils.print_indented(' - tilting')
            w, h = splash.size
            splash = splash.resize((int(w * 0.98), int(h * 1.05)))

        elif champ_name == 'Ezreal':
            Utils.print_indented(' - oldifying')
            splash = Image.open(f'{Utils.path_manual_image_overrides}Ezreal_old.jpg').convert('RGB')

        elif champ_name == 'Galio':
            Utils.print_indented(' - darkening')
            splash = Image.open(f'{Utils.path_manual_image_overrides}Galio_gradient2.bmp').convert('RGB')

        elif champ_name == 'Orianna':
            Utils.print_indented(' - tilting')
            splash = ImageChops.offset(splash, 0, 100)
            splash = splash.rotate(9)

        elif champ_name == 'Ornn':
            Utils.print_indented(' - darkening')
            splash = ImageEnhance.Brightness(splash)
            splash = splash.enhance(0.90)
            Utils.print_indented(' - blurring')
            splash = ImageEnhance.Sharpness(splash)
            splash = splash.enhance(0.00)

        elif champ_name == 'Pyke':
            Utils.print_indented(' - darkening')
            splash = ImageEnhance.Sharpness(splash)
            splash = splash.enhance(0.00)

        elif champ_name == 'Ryze':
            Utils.print_indented(' - tilting')
            splash = splash.rotate(24)

        return splash


    def splash_crop(self, champ_name, splash):
        if not champ_name in IMAGE_TRANSFORMATIONS:
            return splash
        
        if not IMAGE_TRANSFORMATIONS[champ_name].crop_coords != None:
            return splash
        
        Utils.print_indented(' - cropping splash')

        coords = IMAGE_TRANSFORMATIONS[champ_name].crop_coords
        if (coords[2] == 'w'):
            coords = (coords[0], coords[1], splash.size[0], coords[3])

        if (coords[3] == 'h'):
            coords = (coords[0], coords[1], coords[2], splash.size[1])

        return splash.crop(coords)


    def icon_resize(self, champ_name, icon):
        if champ_name not in IMAGE_TRANSFORMATIONS:
            return icon

        scale_factor = IMAGE_TRANSFORMATIONS[champ_name].icon_scale

        if scale_factor == 1.00:
            return icon

        Utils.print_indented(' - scaling icon')

        w, h = icon.size
        w = round(w * scale_factor)
        h = round(h * scale_factor)
        icon = icon.resize((w, h))

        return icon


    def icon_manual_override(self, champ_name, icon):
        """
        Manually overrides some very low % match rate icons to more
        recognisable forms.
        """

        if champ_name == 'Akali':
            Utils.print_indented(' - finding icon')
            icon = Image.open(f'{Utils.path_manual_image_overrides}Akali_icon.bmp')

        elif champ_name == 'Aphelios':
            Utils.print_indented(' - finding icon')
            icon = Image.open(f'{Utils.path_manual_image_overrides}Aphelios_icon.bmp')

        elif champ_name == 'Mordekaiser':
            Utils.print_indented(' - finding icon')
            icon = Image.open(f'{Utils.path_manual_image_overrides}Mordekaiser_icon.bmp')

        elif champ_name == 'Pyke':
            Utils.print_indented(' - finding icon')
            icon = Image.open(f'{Utils.path_manual_image_overrides}Pyke_icon.bmp')

        elif champ_name == 'Rakan':
            Utils.print_indented(' - finding icon')
            icon = Image.open(f'{Utils.path_manual_image_overrides}Rakan_icon.bmp')

        return icon


    def check_missing_champions(self):
        missing = [champ for champ in Utils.read_champlist_from_file() if champ not in IMAGE_TRANSFORMATIONS]
        print('----')
        print(f'\nMissing champion settings: {missing}')