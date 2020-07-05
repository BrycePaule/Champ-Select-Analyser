import os
import urllib.request

from PIL import Image, ImageOps
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from contextlib import suppress

from ImageEditor import ImageEditor


class Downloader():

    def __init__(self):
        self.IEdit = ImageEditor()

        self.splash_path = 'D:/Scripts/Python/ChampSelectAnalyser/Splashes_Raw/'
        self.icon_path = 'D:/Scripts/Python/ChampSelectAnalyser/Icons_Raw/'

        self.champlist_filename = 'champlist.txt'

        self.champlist_url = 'https://na.leagueoflegends.com/en-us/champions/'
        self.splash_url_prefix = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/'
        self.splash_url_suffix = '_0.jpg'
        self.icon_url_prefix = 'https://lol.gamepedia.com/File:'
        self.icon_url_suffix = 'Square.png'


    """ SCRAPING """

    def scrape_champlist_raw(self):
        """ Scrapes raw champlist from league of legends website. """

        uClient = uReq(self.champlist_url)
        page_html = uClient.read()
        uClient.close()

        page = BeautifulSoup(page_html, 'html.parser')
        names = page.select('.style__Name-sc-12h96bu-2')
        champlist_raw = [name.get_text() for name in names]

        champlist_for_splash_download = []
        for name in champlist_raw:
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


    def scrape_splashes(self, champlist, download=False):
        """
        Scrapes raw splash arts from league of legends website.  Makes
        necessary crops + edits to each splash, and saves an inverted copy
        of each to file.
        """

        for name in champlist:
            if download:
                url = self.splash_url_prefix + name + self.splash_url_suffix
                name = self.convert_to_save_name(name)
                print('Downloading splash: ' + name)
                urllib.request.urlretrieve(url, 'Splashes_Raw/' + name + '.bmp')
            else:
                name = self.convert_to_save_name(name)
                print('Fixing splash: ' + name)

            splash = Image.open(self.splash_path + name + '.bmp')
            splash = self.IEdit.faceCover(name, splash)
            splash = self.IEdit.fixSplashes(name, splash)
            splash = self.IEdit.scaleSplash(name, splash)
            splash.save('Splashes/' + name + '.bmp')
            splash = ImageOps.mirror(splash)
            splash.save('Splashes/' + name + '_inverted.bmp')


    def scrape_icons(self, champlist, download=False):
        """
        Scrapes raw icons arts from wiki website.  Makes necessary crops +
        edits and saves a single copy of each to file (icons don't get flipped
        in champion select)
        """

        for name in champlist:

            if download:
                url = self.icon_url_prefix + name + self.icon_url_suffix
                name = self.convert_to_save_name(name)

                uClient = uReq(url)
                page_html = uClient.read()
                uClient.close()

                soup = BeautifulSoup(page_html, 'html.parser')
                image_url = soup.find(id='file').a.get('href')
                print('Downloading icon: ' + name)
                urllib.request.urlretrieve(image_url, 'Icons_Raw/' + name + '.bmp')
            else:
                name = self.convert_to_save_name(name)
                print('Fixing icon: ' + name)

            icon = Image.open(self.icon_path + name + '.bmp')
            icon = self.IEdit.fixIcons(name, icon)
            icon = self.IEdit.scaleIcon(name, icon)
            icon.save('Icons/' + name + '.bmp')
            icon = ImageOps.mirror(icon)
            icon.save('Icons/' + name + '_inverted.bmp')


    """ CHAMPLIST """

    def get_champlist_for_saving(self, champlist):
        champlist_fixed = []

        for name in champlist:
            name = name.replace("Chogath", 'ChoGath')
            name = name.replace("Kaisa", 'KaiSa')
            name = name.replace("Khazix", 'KhaZix')
            name = name.replace("Leblanc", 'LeBlanc')
            name = name.replace("MonkeyKing", 'Wukong')
            name = name.replace("Velkoz", 'VelKoz')
            champlist_fixed.append(name)

        with suppress(FileNotFoundError):
            os.remove(self.champlist_filename)

        with open(self.champlist_filename, 'x') as f:
            for name in champlist_fixed:
                f.write(name + '\n')

        return champlist_fixed


    def get_champlist_for_icon_download(self, champlist):
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


    """ NAMING """

    def convert_to_save_name(self, name):
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