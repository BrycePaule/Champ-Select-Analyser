import os
import Utils

from PIL import Image, ImageOps, ImageChops, ImageDraw, ImageEnhance

from scales import image_scales


class ImageEditor:

    """
    Contains all methods to correct differences between broadcast graphics
    and default splash arts / icons.

    Includes cropping, tilting, enhancing, darkening, covering unwanted champ
    portraits, mirroring, etc.

    """

    def __init__(self):
        self.text_spacer = ' ' * 24
        self.champlist = Utils.read_champlist_from_file()

        self.splash_raw_path = f'./Assets/Splashes_Raw/'
        self.splash_path = f'./Assets/Splashes/'
        self.icon_raw_path = f'./Assets/Icons_Raw/'
        self.icon_path = f'./Assets/Icons/'
        self.manual_override_path = f'./Assets/Manual_Image_Overrides/'

        self.check_missing_champions()
        self.init_directories()


    def init_directories(self):
        os.makedirs(self.splash_raw_path, exist_ok = True)
        os.makedirs(self.splash_path, exist_ok = True)
        os.makedirs(self.icon_raw_path, exist_ok = True)
        os.makedirs(self.icon_path, exist_ok = True)
        os.makedirs(self.manual_override_path, exist_ok = True)


    """ IMAGE EDITING """

    def optimise_splashes(self, champ_name):
        splash = Image.open(self.splash_raw_path + champ_name + '.bmp')

        splash = self.splash_blockout_secondaries(champ_name, splash)
        splash = self.splash_manual_overrides(champ_name, splash)
        splash = self.splash_crop(champ_name, splash)
        splash = self.splash_resize(champ_name, splash)

        splash.save(self.splash_path + champ_name + '.bmp')
        splash = ImageOps.mirror(splash)
        splash.save(self.splash_path + champ_name + '_inverted.bmp')


    def optimise_icons(self, champ_name):
        icon = Image.open(self.icon_raw_path + champ_name + '.bmp')

        icon = self.icon_manual_override(champ_name, icon)
        icon = self.icon_resize(champ_name, icon)

        icon.save(self.icon_path + champ_name + '.bmp', 'bmp')
        icon = ImageOps.mirror(icon)
        icon.save(self.icon_path + champ_name + '_inverted.bmp', 'bmp')


    def splash_resize(self, champ_name, splash):
        if champ_name not in image_scales:
            return splash

        scale_factor = image_scales[champ_name].splash_scale

        if scale_factor == 1.00:
            return splash

        print(f'{self.text_spacer} - scaling splash')

        w, h = splash.size
        w = round(w * scale_factor)
        h = round(h * scale_factor)
        splash = splash.resize((w, h))

        return splash


    def splash_blockout_secondaries(self, champ_name, splash):
        #  Blocks out unwanted champions from dual champion splashes. 

        if champ_name == 'Xayah':
            print(f'{self.text_spacer} - blocking out Rakan')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(400, 20), (600, 200)], 'black')

        elif champ_name == 'Rakan':
            print(f'{self.text_spacer} - blocking out Xayah')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(300, 120), (500, 300)], 'black')

        elif champ_name == 'Kayle':
            print(f'{self.text_spacer} - blocking out Morgana')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(200, 120), (500, 300)], 'black')

        elif champ_name == 'Morgana':
            print(f'{self.text_spacer} - blocking out Kayle')
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
            print(f'{self.text_spacer} - tilting')
            splash = splash.rotate(2)

        elif champ_name == 'Corki':
            print(f'{self.text_spacer} - tilting')
            w, h = splash.size
            splash = splash.resize((int(w * 0.98), int(h * 1.05)))

        elif champ_name == 'Ezreal':
            print(f'{self.text_spacer} - oldifying')
            splash = Image.open(f'{self.manual_override_path}Ezreal_old.jpg').convert('RGB')

        elif champ_name == 'Galio':
            print(f'{self.text_spacer} - darkening')
            splash = Image.open(f'{self.manual_override_path}Galio_gradient2.bmp').convert('RGB')

        elif champ_name == 'Orianna':
            print(f'{self.text_spacer} - tilting')
            splash = ImageChops.offset(splash, 0, 100)
            splash = splash.rotate(9)

        elif champ_name == 'Ornn':
            print(f'{self.text_spacer} - darkening')
            splash = ImageEnhance.Brightness(splash)
            splash = splash.enhance(0.90)
            print(f'{self.text_spacer} - blurring')
            splash = ImageEnhance.Sharpness(splash)
            splash = splash.enhance(0.00)

        elif champ_name == 'Pyke':
            print(f'{self.text_spacer} - darkening')
            splash = ImageEnhance.Sharpness(splash)
            splash = splash.enhance(0.00)

        elif champ_name == 'Ryze':
            print(f'{self.text_spacer} - tilting')
            splash = splash.rotate(24)

        return splash


    def splash_crop(self, champ_name, splash):
        if not champ_name in image_scales:
            return splash
        
        if not image_scales[champ_name].crop != None:
            return splash
        
        print(f'{self.text_spacer} - cropping splash')

        coords = image_scales[champ_name].crop
        if (coords[2] == 'w'):
            coords = (coords[0], coords[1], splash.size[0], coords[3])

        if (coords[3] == 'h'):
            coords = (coords[0], coords[1], coords[2], splash.size[1])

        return splash.crop(coords)


    def icon_resize(self, champ_name, icon):
        if champ_name not in image_scales:
            return icon

        scale_factor = image_scales[champ_name].icon_scale

        if scale_factor == 1.00:
            return icon

        print(f'{self.text_spacer} - scaling icon')

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
            print(f'{self.text_spacer} - finding icon')
            icon = Image.open(f'{self.manual_override_path}Akali_icon.bmp')

        elif champ_name == 'Aphelios':
            print(f'{self.text_spacer} - finding icon')
            icon = Image.open(f'{self.manual_override_path}Aphelios_icon.bmp')

        elif champ_name == 'Mordekaiser':
            print(f'{self.text_spacer} - finding icon')
            icon = Image.open(f'{self.manual_override_path}Mordekaiser_icon.bmp')

        elif champ_name == 'Pyke':
            print(f'{self.text_spacer} - finding icon')
            icon = Image.open(f'{self.manual_override_path}Pyke_icon.bmp')

        elif champ_name == 'Rakan':
            print(f'{self.text_spacer} - finding icon')
            icon = Image.open(f'{self.manual_override_path}Rakan_icon.bmp')

        return icon


    def check_missing_champions(self):
        missing = [champ for champ in Utils.read_champlist_from_file() if champ not in image_scales]
        print('----')
        print(f'\nMissing champion settings: {missing}')