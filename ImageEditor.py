from PIL import Image, ImageOps, ImageChops, ImageDraw, ImageEnhance


splash_scales = {
    'Aatrox': 1.03,
    'Ahri': 1.00,
    'Akali': 1.01,
    'Alistar': 0.65,
    'Amumu': 1.00,
    'Anivia': 1.00,
    'Annie': 1.00,
    'Aphelios': 1.20,
    'Ashe': 1.15,
    'AurelionSol': 1.00,
    'Azir': 1.84,
    'Bard': 1.45,
    'Blitzcrank': 1.05,
    'Brand': 1.33,
    'Braum': 1.50,
    'Caitlyn': 1.30,
    'Camille': 1.14,
    'Cassiopeia': 0.87,
    'ChoGath': 1.00,
    'Corki': 0.96,
    'Darius': 1.00,
    'Diana': 1.30,
    'DrMundo': 1.00,
    'Draven': 1.00,
    'Ekko': 1.00,
    'Elise': 2.35,
    'Evelynn': 1.00,
    'Ezreal': 0.61,
    'Fiddlesticks': 1.00,
    'Fiora': 1.00,
    'Fizz': 1.00,
    'Galio': 1.74,
    'Gangplank': 0.90,
    'Garen': 1.00,
    'Gnar': 0.63,
    'Gragas': 1.10,
    'Graves': 1.00,
    'Hecarim': 1.00,
    'Heimerdinger': 1.00,
    'Illaoi': 1.35,
    'Irelia': 1.37,
    'Ivern': 0.62,
    'Janna': 1.25,
    'JarvanIV': 1.12,
    'Jax': 1.00,
    'Jayce': 1.40,
    'Jhin': 1.00,
    'Jinx': 1.34,
    'KaiSa': 1.30,
    'Kalista': 1.25,
    'Karma': 1.35,
    'Karthus': 1.50,
    'Kassadin': 0.82,
    'Katarina': 1.00,
    'Kayle': 2.30,
    'Kayn': 1.00,
    'Kennen': 0.65,
    'KhaZix': 1.00,
    'Kindred': 1.37,
    'Kled': 0.68,
    'KogMaw': 0.47,
    'LeBlanc': 1.17,
    'LeeSin': 1.60,
    'Leona': 1.46,
    'Lissandra': 1.83,
    'Lucian': 1.64,
    'Lulu': 0.95,
    'Lux': 1.06,
    'Malphite': 1.00,
    'Malzahar': 1.00,
    'Maokai': 0.81,
    'MasterYi': 1.00,
    'MissFortune': 1.21,
    'Mordekaiser': 1.11,
    'Morgana': 2.10,
    'Nami': 1.35,
    'Nasus': 1.00,
    'Nautilus': 0.67,
    'Neeko': 0.77,
    'Nidalee': 1.75,
    'Nocturne': 0.97,
    'Nunu': 1.00,
    'Olaf': 1.03,
    'Orianna': 0.90,
    'Ornn': 1.03,
    'Pantheon': 1.02,
    'Poppy': 0.71,
    'Pyke': 1.05,
    'Qiyana': 0.92,
    'Quinn': 1.20,
    'Rakan': 1.04,
    'Rammus': 1.00,
    'RekSai': 0.65,
    'Renekton': 0.71,
    'Rengar': 1.00,
    'Riven': 1.00,
    'Rumble': 0.86,
    'Ryze': 0.84,
    'Sejuani': 1.51,
    'Senna': 1.05,
    'Sett': 1.25,
    'Shaco': 1.00,
    'Shen': 1.30,
    'Shyvana': 1.00,
    'Singed': 1.00,
    'Sion': 1.30,
    'Sivir': 1.00,
    'Skarner': 1.00,
    'Sona': 1.00,
    'Soraka': 1.08,
    'Swain': 1.00,
    'Sylas': 1.07,
    'Syndra': 1.49,
    'TahmKench': 0.36,
    'Taliyah': 0.70,
    'Talon': 1.00,
    'Taric': 1.15,
    'Teemo': 1.00,
    'Thresh': 1.14,
    'Tristana': 0.60,
    'Trundle': 1.00,
    'Tryndamere': 0.96,
    'TwistedFate': 1.00,
    'Twitch': 1.00,
    'Udyr': 1.00,
    'Urgot': 1.00,
    'Varus': 1.10,
    'Vayne': 1.30,
    'Veigar': 1.00,
    'VelKoz': 0.62,
    'Vi': 1.00,
    'Viktor': 1.22,
    'Vladimir': 1.20,
    'Volibear': 1.32,
    'Warwick': 1.00,
    'Wukong': 1.00,
    'Xayah': 1.00,
    'Xerath': 1.00,
    'XinZhao': 1.10,
    'Yasuo': 1.60,
    'Yorick': 1.00,
    'Yuumi': 0.55,
    'Zac': 0.70,
    'Zed': 1.00,
    'Ziggs': 0.60,
    'Zilean': 1.30,
    'Zoe': 0.78,
    'Zyra': 1.00
}

icon_scales = {
    'Aatrox': 0.80,
    'Ahri': 0.80,
    'Akali': 0.88,
    'Alistar': 0.80,
    'Amumu': 0.80,
    'Anivia': 0.80,
    'Annie': 0.80,
    'Aphelios': 0.81,
    'Ashe': 0.80,
    'AurelionSol': 0.80,
    'Azir': 0.76,
    'Bard': 0.76,
    'Blitzcrank': 0.72,
    'Brand': 0.80,
    'Braum': 0.80,
    'Caitlyn': 0.80,
    'Camille': 0.80,
    'Cassiopeia': 0.80,
    'ChoGath': 0.80,
    'Corki': 0.80,
    'Darius': 0.80,
    'Diana': 0.80,
    'DrMundo': 0.80,
    'Draven': 0.80,
    'Ekko': 0.80,
    'Elise': 0.80,
    'Evelynn': 0.80,
    'Ezreal': 0.80,
    'Fiddlesticks': 0.80,
    'Fiora': 0.80,
    'Fizz': 0.80,
    'Galio': 0.80,
    'Gangplank': 0.80,
    'Garen': 0.80,
    'Gnar': 0.80,
    'Gragas': 0.80,
    'Graves': 0.80,
    'Hecarim': 0.80,
    'Heimerdinger': 0.80,
    'Illaoi': 0.80,
    'Irelia': 0.80,
    'Ivern': 0.80,
    'Janna': 0.80,
    'JarvanIV': 0.74,
    'Jax': 0.80,
    'Jayce': 0.80,
    'Jhin': 0.80,
    'Jinx': 0.80,
    'KaiSa': 0.80,
    'Kalista': 0.80,
    'Karma': 0.76,
    'Karthus': 0.67,
    'Kassadin': 0.80,
    'Katarina': 0.80,
    'Kayle': 0.80,
    'Kayn': 0.80,
    'Kennen': 0.75,
    'KhaZix': 0.80,
    'Kindred': 0.80,
    'Kled': 0.80,
    'KogMaw': 0.80,
    'LeBlanc': 0.74,
    'LeeSin': 0.80,
    'Leona': 0.80,
    'Lissandra': 0.70,
    'Lucian': 0.75,
    'Lulu': 0.80,
    'Lux': 0.80,
    'Malphite': 0.80,
    'Malzahar': 0.80,
    'Maokai': 0.80,
    'MasterYi': 0.80,
    'MissFortune': 0.80,
    'Mordekaiser': 0.78,
    'Morgana': 0.76,
    'Nami': 0.80,
    'Nasus': 0.80,
    'Nautilus': 0.78,
    'Neeko': 0.80,
    'Nidalee': 0.80,
    'Nocturne': 0.80,
    'Nunu': 0.80,
    'Olaf': 0.75,
    'Orianna': 0.73,
    'Ornn': 0.75,
    'Pantheon': 0.80,
    'Poppy': 0.80,
    'Pyke': 0.88,
    'Qiyana': 0.70,
    'Quinn': 0.80,
    'Rakan': 0.87,
    'Rammus': 0.80,
    'RekSai': 0.80,
    'Renekton': 0.75,
    'Rengar': 0.80,
    'Riven': 0.80,
    'Rumble': 0.75,
    'Ryze': 0.80,
    'Sejuani': 0.76,
    'Senna': 0.72,
    'Sett': 0.70,
    'Shaco': 0.80,
    'Shen': 0.80,
    'Shyvana': 0.80,
    'Singed': 0.80,
    'Sion': 0.80,
    'Sivir': 0.80,
    'Skarner': 0.80,
    'Sona': 0.80,
    'Soraka': 0.80,
    'Swain': 0.80,
    'Sylas': 0.80,
    'Syndra': 0.80,
    'TahmKench': 0.76,
    'Taliyah': 0.75,
    'Talon': 0.80,
    'Taric': 0.80,
    'Teemo': 0.80,
    'Thresh': 0.85,
    'Tristana': 0.80,
    'Trundle': 0.80,
    'Tryndamere': 0.80,
    'TwistedFate': 0.80,
    'Twitch': 0.80,
    'Udyr': 0.80,
    'Urgot': 0.80,
    'Varus': 0.74,
    'Vayne': 0.80,
    'Veigar': 0.80,
    'VelKoz': 0.80,
    'Vi': 0.80,
    'Viktor': 0.75,
    'Vladimir': 0.80,
    'Volibear': 0.80,
    'Warwick': 0.80,
    'Wukong': 0.80,
    'Xayah': 0.80,
    'Xerath': 0.80,
    'XinZhao': 0.80,
    'Yasuo': 0.80,
    'Yorick': 0.80,
    'Yuumi': 0.72,
    'Zac': 0.75,
    'Zed': 0.80,
    'Ziggs': 0.80,
    'Zilean': 0.80,
    'Zoe': 0.67,
    'Zyra': 0.80
}


class ImageEditor():

    """
    Contains all methods to correct differences between broadcast graphics
    and default splash arts / icons.

    Includes cropping, tilting, enhancing, darkening, covering secondary champ
    portraits, mirroring, etc.
    """

    def __init__(self):
        self.splash_raw_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Splashes_Raw/'
        self.splash_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Splashes/'
        self.icon_raw_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Icons_Raw/'
        self.icon_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Icons_Raw/'
        self.manual_override_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Manual_Image_Overrides/'
        self.champlist_path = 'D:/Scripts/Python/ChampSelectAnalyser/champlist.txt'

        self.champlist = self.import_champlist()


    """ IMAGE EDITING """

    def splash_complete_fix(self, champ_name):
        """ Runs all splash art image editing methods, saves results """

        splash = Image.open(self.splash_raw_path + champ_name + '.bmp')

        splash = self.splash_face_cover(champ_name, splash)
        splash = self.splash_edit(champ_name, splash)
        splash = self.splash_scale(champ_name, splash)

        splash.save(self.splash_path + champ_name + '.bmp')
        splash = ImageOps.mirror(splash)
        splash.save(self.splash_path + champ_name + '_inverted.bmp')


    def icon_complete_fix(self, champ_name):
        """ Runs all icon image editing methods, saves results """

        icon = Image.open(self.icon_raw_path + champ_name + '.bmp')

        icon = self.icon_manual_override(champ_name, icon)
        icon = self.icon_scale(champ_name, icon)

        icon.save(self.icon_path + champ_name + '.bmp')
        icon = ImageOps.mirror(icon)
        icon.save(self.icon_path + champ_name + '_inverted.bmp')


    def splash_scale(self, champ_name, splash):
        """ Scales given splash by it's specific scale factor. """

        scale_factor = splash_scales[champ_name]

        if scale_factor != 1.00:
            print('                         - scaling splash')

            w, h = splash.size
            w = round(w * scale_factor)
            h = round(h * scale_factor)

            resized_img = splash.resize((w, h))
        else:
            resized_img = splash

        return resized_img


    def splash_face_cover(self, champ_name, splash):
        """ Blocks out unwanted champions from dual champion splashes. """

        if champ_name == 'Xayah':
            print('                         - blocking out Rakan')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(400, 20), (600, 200)], 'black')

        elif champ_name == 'Rakan':
            print('                         - blocking out Xayah')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(300, 120), (500, 300)], 'black')

        elif champ_name == 'Kayle':
            print('                         - blocking out Morgana')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(200, 120), (500, 300)], 'black')

        elif champ_name == 'Morgana':
            print('                         - blocking out Kayle')
            draw = ImageDraw.Draw(splash)
            draw.rectangle([(200, 120), (500, 300)], 'black')

        return splash


    def splash_edit(self, champ_name, splash):
        """
        Crops and edits each splash to be recognisable by its crop.

        Some splashes get rotated / edited by broadcast graphic teams for
        better showing in champion select, this converts the raw splash arts
        to a much closer form that's used on broadcast to be able to match.
        """

        # INDEX = 16
        if champ_name == 'Camille':
            print('                         - tilting')
            splash = splash.rotate(2)

        elif champ_name == 'Corki':
            print('                         - tilting')
            w, h = splash.size
            splash = splash.resize((int(w * 0.98), int(h * 1.05)))

        elif champ_name == 'Ezreal':
            print('                         - oldifying')
            splash = Image.open(f'{self.manual_override_path}Ezreal_old.jpg').convert('RGB')

        elif champ_name == 'Galio':
            print('                         - darkening')
            splash = Image.open(f'{self.manual_override_path}Galio_gradient2.bmp').convert('RGB')

        # INDEX = 83
        elif champ_name == 'Orianna':
            print('                         - tilting')
            splash = ImageChops.offset(splash, 0, 100)
            splash = splash.rotate(9)

        # INDEX = 85
        elif champ_name == 'Ornn':
            print('                         - darkening')
            splash = ImageEnhance.Brightness(splash)
            splash = splash.enhance(0.90)
            print('                         - blurring')
            splash = ImageEnhance.Sharpness(splash)
            splash = splash.enhance(0.00)

        elif champ_name == 'Pyke':
            print('                         - darkening')
            splash = ImageEnhance.Sharpness(splash)
            splash = splash.enhance(0.00)

        elif champ_name == 'Ryze':
            print('                         - tilting')
            splash = splash.rotate(24)

        # the changes below crop out largely irrelevant parts of the splash arts,
        # improving search time drastically
        if champ_name == 'Aatrox':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Ahri':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Akali':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Alistar':
            print('                         - cropping splash')
            splash = splash.crop((500, 100, 1000, 600))

        elif champ_name == 'Amumu':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Anivia':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Annie':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Aphelios':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Ashe':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'AurelionSol':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Azir':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Bard':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Blitzcrank':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Brand':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Braum':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Caitlyn':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Camille':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Cassiopeia':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'ChoGath':
            print('                         - cropping splash')
            splash = splash.crop((400, 100, 1100, 600))

        elif champ_name == 'Corki':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Darius':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Diana':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Draven':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'DrMundo':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Ekko':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Elise':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Evelynn':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        # Ez uses manual splash, can't be cropped by the same structure
        # elif champ_name == 'Ezreal':
        # 	print(        '             ... cropping splash')
        # 	splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Fiddlesticks':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Fiora':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Fizz':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Galio':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Gangplank':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Garen':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Gnar':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Gragas':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Graves':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Hecarim':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Heimerdinger':
            print('                         - cropping splash')
            w, h = splash.size
            splash = splash.crop((400, 000, w, h))

        elif champ_name == 'Illaoi':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Irelia':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Ivern':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Janna':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'JarvanIV':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Jax':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Jayce':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Jhin':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Jinx':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'KaiSa':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Kalista':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Karma':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Karthus':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Kassadin':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1100, 500))

        elif champ_name == 'Katarina':
            print('                         - cropping splash')
            splash = splash.crop((500, 100, 1000, 600))

        elif champ_name == 'Kayle':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Kayn':
            print('                         - cropping splash')
            splash = splash.crop((400, 100, 900, 600))

        elif champ_name == 'Kennen':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1200, 500))

        elif champ_name == 'KhaZix':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Kindred':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Kled':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1200, 500))

        elif champ_name == 'KogMaw':
            print('                         - cropping splash')
            w, h = splash.size
            splash = splash.crop((500, 000, w, h))

        elif champ_name == 'LeBlanc':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'LeeSin':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Leona':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Lissandra':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Lucian':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Lulu':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Lux':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Malphite':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1100, 600))

        elif champ_name == 'Malzahar':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Maokai':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'MasterYi':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'MissFortune':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Mordekaiser':
            print('                         - cropping splash')
            splash = splash.crop((300, 000, 800, 500))

        elif champ_name == 'Morgana':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Nami':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Nasus':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Nautilus':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1200, 500))

        elif champ_name == 'Neeko':
            print('                         - cropping splash')
            splash = splash.crop((300, 000, 900, 500))

        elif champ_name == 'Nidalee':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Nocturne':
            print('                         - cropping splash')
            splash = splash.crop((500, 100, 1000, 600))

        # Unsure where the crop starts for Nunu in new splash - update needed later
        # elif champ_name == 'Nunu':
        # 	print(        '             ... cropping splash')
        # 	splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Olaf':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Orianna':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Ornn':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Pantheon':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Poppy':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1100, 500))

        elif champ_name == 'Pyke':
            print('                         - cropping splash')
            splash = splash.crop((300, 000, 800, 500))

        elif champ_name == 'Qiyana':
            print('                         - cropping splash')
            splash = splash.crop((300, 000, 800, 500))

        elif champ_name == 'Quinn':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Rakan':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Rammus':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'RekSai':
            print('                         - cropping splash')
            splash = splash.crop((400, 100, 900, 600))

        elif champ_name == 'Renekton':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 1000, 500))

        elif champ_name == 'Rengar':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Riven':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Rumble':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Ryze':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1200, 500))

        elif champ_name == 'Sejuani':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Senna':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Sett':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Shaco':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Shen':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Shyvana':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Singed':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Sion':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Sivir':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Skarner':
            print('                         - cropping splash')
            splash = splash.crop((600, 100, 1200, 600))

        elif champ_name == 'Sona':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Soraka':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Swain':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Sylas':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Syndra':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'TahmKench':
            print('                         - cropping splash')
            w, h = splash.size
            splash = splash.crop((200, 000, w, h))

        elif champ_name == 'Taliyah':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Talon':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Taric':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Teemo':
            print('                         - cropping splash')
            w, h = splash.size
            splash = splash.crop((400, 000, w, (h - 100)))

        elif champ_name == 'Thresh':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Tristana':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1100, 500))

        elif champ_name == 'Trundle':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Tryndamere':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'TwistedFate':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Twitch':
            print('                         - cropping splash')
            splash = splash.crop((500, 100, 1000, 600))

        elif champ_name == 'Udyr':
            print('                         - cropping splash')
            splash = splash.crop((400, 100, 900, 600))

        elif champ_name == 'Urgot':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Varus':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Vayne':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Veigar':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1100, 500))

        elif champ_name == 'VelKoz':
            print('                         - cropping splash')
            w, h = splash.size
            splash = splash.crop((300, 000, w, (h - 100)))

        elif champ_name == 'Vi':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Viktor':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Vladimir':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        # champ reworked, this will need to be updated
        elif champ_name == 'Volibear':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Warwick':
            print('                         - cropping splash')
            splash = splash.crop((500, 200, 1100, 700))

        elif champ_name == 'Wukong':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Xayah':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Xerath':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'XinZhao':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Yasuo':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        elif champ_name == 'Yorick':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Yuumi':
            print('                         - cropping splash')
            splash = splash.crop((200, 000, 900, 400))

        elif champ_name == 'Zac':
            print('                         - cropping splash')
            splash = splash.crop((600, 200, 1100, 700))

        elif champ_name == 'Zed':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1100, 500))

        elif champ_name == 'Ziggs':
            print('                         - cropping splash')
            splash = splash.crop((600, 000, 1200, 500))

        elif champ_name == 'Zilean':
            print('                         - cropping splash')
            splash = splash.crop((500, 000, 1000, 500))

        elif champ_name == 'Zoe':
            print('                         - cropping splash')
            splash = splash.crop((400, 000, 900, 500))

        elif champ_name == 'Zyra':
            print('                         - cropping splash')
            splash = splash.crop((700, 000, 1200, 500))

        return splash


    def icon_scale(self, champ_name, icon):
        """ Scales given icon by it's specific scale factor. """

        scale_factor = icon_scales[champ_name]

        if scale_factor != 1.00:
            print('                         - scaling icon')

            w, h = icon.size
            w = round(w * scale_factor)
            h = round(h * scale_factor)

            resized_img = icon.resize((w, h))
        else:
            resized_img = icon

        return resized_img


    def icon_manual_override(self, champ_name, icon):
        """
        Manually overrides some very low % match rate icons to more
        recognisable forms.
        """

        if champ_name == 'Akali':
            print('                         - finding icon')
            icon = Image.open(f'{self.manual_override_path}Akali_icon.bmp')

        elif champ_name == 'Aphelios':
            print('                         - finding icon')
            icon = Image.open(f'{self.manual_override_path}Aphelios_icon.bmp')

        elif champ_name == 'Mordekaiser':
            print('                         - finding icon')
            icon = Image.open(f'{self.manual_override_path}Mordekaiser_icon.bmp')

        elif champ_name == 'Pyke':
            print('                         - finding icon')
            icon = Image.open(f'{self.manual_override_path}Pyke_icon.bmp')

        elif champ_name == 'Rakan':
            print('                         - finding icon')
            icon = Image.open(f'{self.manual_override_path}Rakan_icon.bmp')

        return icon


    """ CHAMPLIST """

    def import_champlist(self):
        """ Imports champlist from file. """

        with open(self.champlist_path, 'r') as f:
            return [name.strip() for name in f]