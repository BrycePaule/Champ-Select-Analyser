import urllib.request
import os
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageOps, ImageChops, ImageEnhance
import time
import datetime
import cProfile

# ------------------------------------------------------------------------------------------
# CONSTANTS

scales = {'Aatrox': 1.03, 'Ahri': 1.00, 'Akali': 1.01, 'Alistar': 0.65,
    'Amumu': 1.00, 'Anivia': 1.00, 'Annie': 1.00, 'Aphelios': 1.20,
    'Ashe': 1.15, 'AurelionSol': 1.00, 'Azir': 1.84, 'Bard': 1.45,
    'Blitzcrank': 1.05, 'Brand': 1.33, 'Braum': 1.50, 'Caitlyn': 1.30,
    'Camille': 1.14, 'Cassiopeia': 0.87, 'ChoGath': 1.00, 'Corki': 0.96,
    'Darius': 1.00, 'Diana': 1.30, 'DrMundo': 1.00, 'Draven': 1.00,
    'Ekko': 1.00, 'Elise': 2.35, 'Evelynn': 1.00, 'Ezreal': 0.61,
    'Fiddlesticks': 1.00, 'Fiora': 1.00, 'Fizz': 1.00, 'Galio': 1.74,
    'Gangplank': 0.90, 'Garen': 1.00, 'Gnar': 0.63, 'Gragas': 1.10,
    'Graves': 1.00, 'Hecarim': 1.00, 'Heimerdinger': 1.00, 'Illaoi': 1.35,
    'Irelia': 1.37, 'Ivern': 0.62, 'Janna': 1.25, 'JarvanIV': 1.12,
    'Jax': 1.00, 'Jayce': 1.40, 'Jhin': 1.00, 'Jinx': 1.34, 'KaiSa': 1.30,
    'Kalista': 1.25, 'Karma': 1.35, 'Karthus': 1.50, 'Kassadin': 0.82,
    'Katarina': 1.00, 'Kayle': 2.30, 'Kayn': 1.00, 'Kennen': 0.65,
    'KhaZix': 1.00, 'Kindred': 1.37, 'Kled': 0.68, 'KogMaw': 0.47,
    'LeBlanc': 1.17, 'LeeSin': 1.60, 'Leona': 1.46, 'Lissandra': 1.83,
    'Lucian': 1.64, 'Lulu': 0.95, 'Lux': 1.06, 'Malphite': 1.00,
    'Malzahar': 1.00, 'Maokai': 0.81, 'MasterYi': 1.00, 'MissFortune': 1.21,
    'Mordekaiser': 1.11, 'Morgana': 2.10, 'Nami': 1.35, 'Nasus': 1.00,
    'Nautilus': 0.67, 'Neeko': 0.77, 'Nidalee': 1.75, 'Nocturne': 0.97,
    'Nunu': 1.00, 'Olaf': 1.03, 'Orianna': 0.90, 'Ornn': 1.03,
    'Pantheon': 1.02, 'Poppy': 0.71, 'Pyke': 1.05, 'Qiyana': 0.92,
    'Quinn': 1.20, 'Rakan': 1.04, 'Rammus': 1.00, 'RekSai': 0.65,
    'Renekton': 0.71, 'Rengar': 1.00, 'Riven': 1.00, 'Rumble': 0.86,
    'Ryze': 0.84, 'Sejuani': 1.51, 'Senna': 1.05, 'Sett': 1.25, 'Shaco': 1.00,
    'Shen': 1.30, 'Shyvana': 1.00, 'Singed': 1.00, 'Sion': 1.30, 'Sivir': 1.00,
    'Skarner': 1.00, 'Sona': 1.00, 'Soraka': 1.08, 'Swain': 1.00,
    'Sylas': 1.07, 'Syndra': 1.49, 'TahmKench': 0.36, 'Taliyah': 0.70,
    'Talon': 1.00, 'Taric': 1.15, 'Teemo': 1.00, 'Thresh': 1.14,
    'Tristana': 0.60, 'Trundle': 1.00, 'Tryndamere': 0.96, 'TwistedFate': 1.00,
    'Twitch': 1.00, 'Udyr': 1.00, 'Urgot': 1.00, 'Varus': 1.10, 'Vayne': 1.30,
    'Veigar': 1.00, 'VelKoz': 0.62, 'Vi': 1.00, 'Viktor': 1.22,
    'Vladimir': 1.20, 'Volibear': 1.32, 'Warwick': 1.00, 'Wukong': 1.00,
    'Xayah': 1.00, 'Xerath': 1.00, 'XinZhao': 1.10, 'Yasuo': 1.60,
    'Yorick': 1.00, 'Yuumi': 0.55, 'Zac': 0.70, 'Zed': 1.00, 'Ziggs': 0.60,
    'Zilean': 1.30, 'Zoe': 0.78, 'Zyra': 1.00}

scales_icons = {'Aatrox': 0.80, 'Ahri': 0.80, 'Akali': 0.88, 'Alistar': 0.80,
    'Amumu': 0.80, 'Anivia': 0.80, 'Annie': 0.80, 'Aphelios': 0.81,
    'Ashe': 0.80, 'AurelionSol': 0.80, 'Azir': 0.76, 'Bard': 0.76,
    'Blitzcrank': 0.72, 'Brand': 0.80, 'Braum': 0.80, 'Caitlyn': 0.80,
    'Camille': 0.80, 'Cassiopeia': 0.80, 'ChoGath': 0.80, 'Corki': 0.80,
    'Darius': 0.80, 'Diana': 0.80, 'DrMundo': 0.80, 'Draven': 0.80,
    'Ekko': 0.80, 'Elise': 0.80, 'Evelynn': 0.80, 'Ezreal': 0.80,
    'Fiddlesticks': 0.80, 'Fiora': 0.80, 'Fizz': 0.80, 'Galio': 0.80,
    'Gangplank': 0.80, 'Garen': 0.80, 'Gnar': 0.80, 'Gragas': 0.80,
    'Graves': 0.80, 'Hecarim': 0.80, 'Heimerdinger': 0.80, 'Illaoi': 0.80,
    'Irelia': 0.80, 'Ivern': 0.80, 'Janna': 0.80, 'JarvanIV': 0.74,
    'Jax': 0.80, 'Jayce': 0.80, 'Jhin': 0.80, 'Jinx': 0.80, 'KaiSa': 0.80,
    'Kalista': 0.80, 'Karma': 0.76, 'Karthus': 0.67, 'Kassadin': 0.80,
    'Katarina': 0.80, 'Kayle': 0.80, 'Kayn': 0.80, 'Kennen': 0.75,
    'KhaZix': 0.80, 'Kindred': 0.80, 'Kled': 0.80, 'KogMaw': 0.80,
    'LeBlanc': 0.74, 'LeeSin': 0.80, 'Leona': 0.80, 'Lissandra': 0.70,
    'Lucian': 0.75, 'Lulu': 0.80, 'Lux': 0.80, 'Malphite': 0.80,
    'Malzahar': 0.80, 'Maokai': 0.80, 'MasterYi': 0.80, 'MissFortune': 0.80,
    'Mordekaiser': 0.78, 'Morgana': 0.76, 'Nami': 0.80, 'Nasus': 0.80,
    'Nautilus': 0.78, 'Neeko': 0.80, 'Nidalee': 0.80, 'Nocturne': 0.80,
    'Nunu': 0.80, 'Olaf': 0.75, 'Orianna': 0.73, 'Ornn': 0.75,
    'Pantheon': 0.80, 'Poppy': 0.80, 'Pyke': 0.88, 'Qiyana': 0.70,
    'Quinn': 0.80, 'Rakan': 0.87, 'Rammus': 0.80, 'RekSai': 0.80,
    'Renekton': 0.75, 'Rengar': 0.80, 'Riven': 0.80, 'Rumble': 0.75,
    'Ryze': 0.80, 'Sejuani': 0.76, 'Senna': 0.72, 'Sett': 0.70, 'Shaco': 0.80,
    'Shen': 0.80, 'Shyvana': 0.80, 'Singed': 0.80, 'Sion': 0.80, 'Sivir': 0.80,
    'Skarner': 0.80, 'Sona': 0.80, 'Soraka': 0.80, 'Swain': 0.80,
    'Sylas': 0.80, 'Syndra': 0.80, 'TahmKench': 0.76, 'Taliyah': 0.75,
    'Talon': 0.80, 'Taric': 0.80, 'Teemo': 0.80, 'Thresh': 0.85,
    'Tristana': 0.80, 'Trundle': 0.80, 'Tryndamere': 0.80, 'TwistedFate': 0.80,
    'Twitch': 0.80, 'Udyr': 0.80, 'Urgot': 0.80, 'Varus': 0.74, 'Vayne': 0.80,
    'Veigar': 0.80, 'VelKoz': 0.80, 'Vi': 0.80, 'Viktor': 0.75,
    'Vladimir': 0.80, 'Volibear': 0.80, 'Warwick': 0.80, 'Wukong': 0.80,
    'Xayah': 0.80, 'Xerath': 0.80, 'XinZhao': 0.80, 'Yasuo': 0.80,
    'Yorick': 0.80, 'Yuumi': 0.72, 'Zac': 0.75, 'Zed': 0.80, 'Ziggs': 0.80,
    'Zilean': 0.80, 'Zoe': 0.67, 'Zyra': 0.80}


# ------------------------------------------------------------------------------------------
# IMAGE MANIPULATION


# covers out the wrong champ in dual splash arts
def faceCover(champ_name, splash_image):
    if (champ_name == 'Xayah'):
        print('                               ... blocking out Rakan')
        draw = ImageDraw.Draw(splash_image)
        draw.rectangle([(400, 20), (600, 200)], 'black')

    if (champ_name == 'Rakan'):
        print('                               ... blocking out Xayah')
        draw = ImageDraw.Draw(splash_image)
        draw.rectangle([(300, 120), (500, 300)], 'black')

    if (champ_name == 'Kayle'):
        print('                               ... blocking out Morgana')
        draw = ImageDraw.Draw(splash_image)
        draw.rectangle([(200, 120), (500, 300)], 'black')

    if (champ_name == 'Morgana'):
        print('                               ... blocking out Kayle')
        draw = ImageDraw.Draw(splash_image)
        draw.rectangle([(200, 120), (500, 300)], 'black')

    return splash_image


# fix discrepancies between default splash arts, and whats used on the LCK
#   -- e.g. Ryze is rotated 24 degrees so that he faces sideways not up
def fixSplashes(champ_name, splash_image):
    # INDEX = 16
    if (champ_name == 'Camille'):
        print('                               ... tilting')
        splash_image = splash_image.rotate(2)

    if (champ_name == 'Corki'):
        print('                               ... tilting')
        w, h = splash_image.size
        splash_image = splash_image.resize((int(w * 0.98), int(h * 1.05)))

    if (champ_name == 'Ezreal'):
        print('                               ... oldifying')
        splash_image = Image.open('ManualImageFixes/Ezreal_old.jpg').convert(
            'RGB')

    if (champ_name == 'Galio'):
        print('                               ... darkening')
        splash_image = Image.open(
            'ManualImageFixes/Galio_gradient2.bmp').convert('RGB')

    # INDEX = 83
    if (champ_name == 'Orianna'):
        print('                               ... tilting')
        splash_image = ImageChops.offset(splash_image, 0, 100)
        splash_image = splash_image.rotate(9)

    # INDEX = 85
    if (champ_name == 'Ornn'):
        print('                               ... darkening')
        splash_image = ImageEnhance.Brightness(splash_image)
        splash_image = splash_image.enhance(0.90)
        print('                               ... blurring')
        splash_image = ImageEnhance.Sharpness(splash_image)
        splash_image = splash_image.enhance(0.00)

    if (champ_name == 'Pyke'):
        print('                               ... darkening')
        splash_image = ImageEnhance.Sharpness(splash_image)
        splash_image = splash_image.enhance(0.00)

    if (champ_name == 'Ryze'):
        print('                               ... tilting')
        splash_image = splash_image.rotate(24)

    # the changes below crop out largely irrelevant parts of the splash arts,
    # improving search time drastically
    if (champ_name == 'Aatrox'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Ahri'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Akali'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Alistar'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 100, 1000, 600))

    if (champ_name == 'Amumu'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Anivia'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Annie'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Aphelios'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Ashe'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'AurelionSol'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Azir'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Bard'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Blitzcrank'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Brand'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Braum'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Caitlyn'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Camille'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Cassiopeia'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'ChoGath'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 100, 1100, 600))

    if (champ_name == 'Corki'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Darius'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Diana'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Draven'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'DrMundo'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Ekko'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Elise'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Evelynn'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    # Ez uses manual splash, can't be cropped by the same structure
    # if (champ_name == 'Ezreal'):
    # 	print('                               ... cropping')
    # 	splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Fiddlesticks'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Fiora'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Fizz'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Galio'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Gangplank'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Garen'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Gnar'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Gragas'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Graves'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Hecarim'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Heimerdinger'):
        print('                               ... cropping')
        w, h = splash_image.size
        splash_image = splash_image.crop((400, 000, w, h))

    if (champ_name == 'Illaoi'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Irelia'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Ivern'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Janna'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'JarvanIV'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Jax'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Jayce'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Jhin'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Jinx'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'KaiSa'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Kalista'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Karma'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Karthus'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Kassadin'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1100, 500))

    if (champ_name == 'Katarina'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 100, 1000, 600))

    if (champ_name == 'Kayle'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Kayn'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 100, 900, 600))

    if (champ_name == 'Kennen'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1200, 500))

    if (champ_name == 'KhaZix'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Kindred'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Kled'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1200, 500))

    if (champ_name == 'KogMaw'):
        print('                               ... cropping')
        w, h = splash_image.size
        splash_image = splash_image.crop((500, 000, w, h))

    if (champ_name == 'LeBlanc'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'LeeSin'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Leona'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Lissandra'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Lucian'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Lulu'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Lux'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Malphite'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1100, 600))

    if (champ_name == 'Malzahar'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Maokai'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'MasterYi'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'MissFortune'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Mordekaiser'):
        print('                               ... cropping')
        splash_image = splash_image.crop((300, 000, 800, 500))

    if (champ_name == 'Morgana'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Nami'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Nasus'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Nautilus'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1200, 500))

    if (champ_name == 'Neeko'):
        print('                               ... cropping')
        splash_image = splash_image.crop((300, 000, 900, 500))

    if (champ_name == 'Nidalee'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Nocturne'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 100, 1000, 600))

    # Unsure where the crop starts for Nunu in new splash - update needed later
    # if (champ_name == 'Nunu'):
    # 	print('                               ... cropping')
    # 	splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Olaf'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Orianna'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Ornn'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Pantheon'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Poppy'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1100, 500))

    if (champ_name == 'Pyke'):
        print('                               ... cropping')
        splash_image = splash_image.crop((300, 000, 800, 500))

    if (champ_name == 'Qiyana'):
        print('                               ... cropping')
        splash_image = splash_image.crop((300, 000, 800, 500))

    if (champ_name == 'Quinn'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Rakan'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Rammus'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'RekSai'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 100, 900, 600))

    if (champ_name == 'Renekton'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 1000, 500))

    if (champ_name == 'Rengar'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Riven'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Rumble'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Ryze'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1200, 500))

    if (champ_name == 'Sejuani'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Senna'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Sett'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Shaco'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Shen'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Shyvana'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Singed'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Sion'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Sivir'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Skarner'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 100, 1200, 600))

    if (champ_name == 'Sona'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Soraka'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Swain'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Sylas'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Syndra'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'TahmKench'):
        print('                               ... cropping')
        w, h = splash_image.size
        splash_image = splash_image.crop((200, 000, w, h))

    if (champ_name == 'Taliyah'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Talon'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Taric'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Teemo'):
        print('                               ... cropping')
        w, h = splash_image.size
        splash_image = splash_image.crop((400, 000, w, (h - 100)))

    if (champ_name == 'Thresh'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Tristana'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1100, 500))

    if (champ_name == 'Trundle'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Tryndamere'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'TwistedFate'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Twitch'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 100, 1000, 600))

    if (champ_name == 'Udyr'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 100, 900, 600))

    if (champ_name == 'Urgot'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Varus'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Vayne'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Veigar'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1100, 500))

    if (champ_name == 'VelKoz'):
        print('                               ... cropping')
        w, h = splash_image.size
        splash_image = splash_image.crop((300, 000, w, (h - 100)))

    if (champ_name == 'Vi'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Viktor'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Vladimir'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Volibear'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Warwick'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 200, 1100, 700))

    if (champ_name == 'Wukong'):
        print('                               ... croppin')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Xayah'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Xerath'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'XinZhao'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Yasuo'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    if (champ_name == 'Yorick'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Yuumi'):
        print('                               ... cropping')
        splash_image = splash_image.crop((200, 000, 900, 400))

    if (champ_name == 'Zac'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 200, 1100, 700))

    if (champ_name == 'Zed'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1100, 500))

    if (champ_name == 'Ziggs'):
        print('                               ... cropping')
        splash_image = splash_image.crop((600, 000, 1200, 500))

    if (champ_name == 'Zilean'):
        print('                               ... cropping')
        splash_image = splash_image.crop((500, 000, 1000, 500))

    if (champ_name == 'Zoe'):
        print('                               ... cropping')
        splash_image = splash_image.crop((400, 000, 900, 500))

    if (champ_name == 'Zyra'):
        print('                               ... cropping')
        splash_image = splash_image.crop((700, 000, 1200, 500))

    return splash_image


# replaces unsearchable icons with manual entries
def fixIcons(champ_name, icon_image):
    if (champ_name == 'Akali'):
        print('                               ... finding icon')
        icon_image = Image.open('ManualImageFixes/Akali_icon.bmp')

    if (champ_name == 'Aphelios'):
        print('                               ... finding icon')
        icon_image = Image.open('ManualImageFixes/Aphelios_icon.bmp')

    if (champ_name == 'Mordekaiser'):
        print('                               ... finding icon')
        icon_image = Image.open('ManualImageFixes/Mordekaiser_icon.bmp')

    if (champ_name == 'Pyke'):
        print('                               ... finding icon')
        icon_image = Image.open('ManualImageFixes/Pyke_icon.bmp')

    if (champ_name == 'Rakan'):
        print('                               ... finding icon')
        icon_image = Image.open('ManualImageFixes/Rakan_icon.bmp')

    return icon_image


# ------------------------------------------------------------------------------------------
# CHAMPLIST CREATION AND MANIPULATION


# scrapes default champlist from website,
# returns editted champlist for splash download
def scrapeChamplist():
    print('Scraping champlist')

    # example_url = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Aatrox_0.jpg'
    champs_url = 'https://na.leagueoflegends.com/en-us/champions/'

    uClient = uReq(champs_url)
    page_html = uClient.read()
    uClient.close()

    page = BeautifulSoup(page_html, 'html.parser')
    names = page.select('.style__Name-sc-12h96bu-2')

    # remove the tags, fill only the names into the list
    champlist_default = [name.get_text() for name in names]

    champlist_for_splash_download = []
    for name in champlist_default:
        name = name.replace(' ', '')
        name = name.replace("'", '')
        name = name.replace(".", '')
        name = name.replace("ChoGath", "Chogath")
        name = name.replace("KaiSa", "Kaisa")
        name = name.replace("VelKoz", "Velkoz")
        name = name.replace("KhaZix", "Khazix")
        name = name.replace("LeBlanc", "Leblanc")
        name = name.replace("Nunu&Willump", 'Nunu')
        name = name.replace("Wukong", 'MonkeyKing')
        champlist_for_splash_download.append(name)

    return champlist_for_splash_download


# fixes champlist for personal filenaming, camel-case
# returns that list, also exports to 'champlist.txt'
def fixAndExportChamplist(champlist):
    print('Exporting champlist.txt')

    champlist_fixed = []
    for name in champlist:
        name = name.replace("Chogath", 'ChoGath')
        name = name.replace("Kaisa", 'KaiSa')
        name = name.replace("Khazix", 'KhaZix')
        name = name.replace("Leblanc", 'LeBlanc')
        name = name.replace("MonkeyKing", 'Wukong')
        name = name.replace("Velkoz", 'VelKoz')
        champlist_fixed.append(name)

    os.remove('champlist.txt')
    with open('champlist.txt', 'x') as f:
        for name in champlist_fixed:
            f.write(name + '\n')

    return champlist_fixed


# fixes champlist specifically for icon download
def fixChamplistForIconDownload(champlist):
    champlist_for_icon_download = []
    for name in champlist:
        name = name.replace('\n', '')
        name = name.replace(' ', '')
        name = name.replace('AurelionSol', 'Aurelion_Sol')
        name = name.replace('Chogath', 'Cho%27Gath')
        name = name.replace('JarvanIV', 'Jarvan_IV')
        name = name.replace('KaiSa', 'Kai%27Sa')
        name = name.replace('KhaZix', 'Kha%27Zix')
        name = name.replace('KogMaw', 'Kog%27Maw')
        name = name.replace('LeeSin', 'Lee_Sin')
        name = name.replace('MasterYi', 'Master_Yi')
        name = name.replace('MissFortune', 'Miss_Fortune')
        name = name.replace('Nunu', 'Nunu_&_Willump')
        name = name.replace('RekSai', 'Rek%27Sai')
        name = name.replace('TahmKench', 'Tahm_Kench')
        name = name.replace('TwistedFate', 'Twisted_Fate')
        name = name.replace('VelKoz', 'Vel%27Koz')
        name = name.replace('XinZhao', 'Xin_Zhao')

        champlist_for_icon_download.append(name)

    return champlist_for_icon_download


# given a name, returns the correct version for saving files
def editNameForSave(name):
    name = name.replace('\n', '')
    name = name.replace('%27', '')
    name = name.replace('_', '')
    name = name.replace("Chogath", 'ChoGath')
    name = name.replace("Kaisa", 'KaiSa')
    name = name.replace("Khazix", 'KhaZix')
    name = name.replace("Leblanc", 'LeBlanc')
    name = name.replace("MonkeyKing", 'Wukong')
    name = name.replace("Nunu&Willump", 'Nunu')
    name = name.replace("Velkoz", 'VelKoz')

    return name


# ------------------------------------------------------------------------------------------
# IMAGE SCRAPING


# if True, downloads files
# if False, skips download, fixes splashes as necessary and saves in new location
def scrapeSplashes(champlist, download_bool):
    for name in champlist:
        if download_bool:
            link = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + name + '_0.jpg'

            name = editNameForSave(name)
            print('Downloading splash: ' + name)

            urllib.request.urlretrieve(link,
                                       'ChampSplashes_untouched/' + name + '.bmp')
        else:
            name = editNameForSave(name)
            print('Fixing splash: ' + name)

        splashpath = 'D:/Scripts/Python/Champ_Select_Analyser/ChampSplashes_untouched/' + name + '.bmp'
        splash = Image.open(splashpath)

        splash = faceCover(name, splash)
        splash = fixSplashes(name, splash)
        splash = scaleSplash(name, splash)
        splash.save('ChampSplashesFixed/' + name + '.bmp')

        splash = ImageOps.mirror(splash)
        splash.save('ChampSplashesFixed/' + name + '_inverted.bmp')


# if True, downloads all icons
# if False, skips download, fixes
def scrapeIcons(champlist, download_bool):
    for name in champlist:

        if download_bool:
            url_prefix = 'https://lol.gamepedia.com/File:'
            url_suffix = 'Square.png'
            link = url_prefix + name + url_suffix

            uClient = uReq(link)
            page_html = uClient.read()
            uClient.close()

            soup = BeautifulSoup(page_html, 'html.parser')
            image_url = soup.find(id='file').a.get('href')

            name = editNameForSave(name)

            print('Downloading icon: ' + name)
            urllib.request.urlretrieve(image_url,
                                       'ChampIcons_untouched/' + name + '.bmp')
        else:
            name = editNameForSave(name)
            print('Fixing icon: ' + name)

        icon_path = 'D:/Scripts/Python/Champ_Select_Analyser/ChampIcons_untouched/' + name + '.bmp'
        icon = Image.open(icon_path)

        icon = fixIcons(name, icon)
        icon = scaleIcon(name, icon)
        icon.save('ChampIconsFixed/' + name + '.bmp')

        icon = ImageOps.mirror(icon)
        icon.save('ChampIconsFixed/' + name + '_inverted.bmp')


# ------------------------------------------------------------------------------------------
# IMAGE SCALING

def scaleSplash(champname, splash_image):
    # gets the scaling factor for champname
    # champs_index = [x[0] for x in scales].index(champname)
    # scale_factor = float(scales[champs_index][1])

    scale_factor = scales[champname]

    if (scale_factor != 1.00):
        print('                               ... scaling')

        w, h = splash_image.size
        w = round(w * scale_factor)
        h = round(h * scale_factor)

        resized_img = splash_image.resize((w, h))
    else:
        resized_img = splash_image

    return resized_img


def scaleIcon(champname, icon_image):
    # gets the scaling factor for champname
    # champs_index = [x[0] for x in scales_icons].index(champname)
    # scale_factor = float(scales_icons[champs_index][1])

    scale_factor = scales_icons[champname]

    if (scale_factor != 1.00):
        print('                               ... scaling')

        w, h = icon_image.size
        w = round(w * scale_factor)
        h = round(h * scale_factor)

        resized_img = icon_image.resize((w, h))
    else:
        resized_img = icon_image

    return resized_img


# ------------------------------------------------------------------------------------------
# MAIN

def main():
    time_start = time.perf_counter()

    # creates necessary list of champs for splash scraping, image scraping, and filenaming
    champlist_for_splash_download = scrapeChamplist()
    champlist = fixAndExportChamplist(champlist_for_splash_download)
    champlist_for_icon_download = fixChamplistForIconDownload(champlist)

    # scrapes splashes/icons, fixes/crops/replaces/blacks-out where necessary
    # saves a normal + inverted copy for matcher to use
    # true = download, false = skip download
    scrapeSplashes(champlist_for_splash_download, False)
    scrapeIcons(champlist_for_icon_download, False)

    time_stop = time.perf_counter()
    elapsed_time = str(datetime.timedelta(seconds=time_stop - time_start, ))
    print()
    print('Runtime: ' + elapsed_time)


# ------------------------------------------------------------------------------------------

# cProfile.run('main()')

main()