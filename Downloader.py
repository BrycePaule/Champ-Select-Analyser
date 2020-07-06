import os
import urllib.request

from PIL import Image, ImageOps
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from contextlib import suppress

from ImageEditor import ImageEditor


class Downloader():

    """
    Scrapes champion list, splash arts and icons from the web, saving them
    locally.

    Splash art website, Icon website and local save naming conventions are
    all different, hence the multiple lists + conversions.

    """

    def __init__(self):
        self.IEdit = ImageEditor()

        self.splash_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Splashes/'
        self.icon_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Icons/'
        self.splash_raw_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Splashes_Raw/'
        self.icon_raw_path = 'D:/Scripts/Python/ChampSelectAnalyser/Assets/Icons_Raw/'

        self.champlist_filename = 'champlist.txt'

        self.champlist_raw = []
        self.champlist_save = []
        self.champlist_splash = []
        self.champlist_icon = []

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
        self.champlist_raw = [name.get_text() for name in names]


    def scrape_splash(self, name):
        """
        Scrapes raw splash arts from league of legends website.  Makes
        necessary crops + edits to each splash, and saves an inverted copy
        of each to file.
        """

        url = self.splash_url_prefix + name + self.splash_url_suffix
        name = self.convert_to_save_name(name)
        urllib.request.urlretrieve(url, f'{self.splash_raw_path}/{name}.bmp')


    def scrape_icon(self, name):
        """
        Scrapes raw icons arts from wiki website.  Makes necessary crops +
        edits and saves a copy  + inverted copy to file
        """

        url = self.icon_url_prefix + name + self.icon_url_suffix
        name = self.convert_to_save_name(name)

        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()

        soup = BeautifulSoup(page_html, 'html.parser')
        image_url = soup.find(id='file').a.get('href')
        urllib.request.urlretrieve(image_url, f'{self.icon_raw_path}/{name}.bmp')


    """ CHAMPLIST """

    def convert_champlist_to_splash(self):
        for name in self.champlist_raw:
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
            self.champlist_splash.append(name)


    def convert_champlist_to_save(self):
        with suppress(FileNotFoundError):
            os.remove(self.champlist_filename)

            with open(self.champlist_filename, 'x') as f:
                for name in self.champlist_raw:
                    name = name.replace(' ', '')
                    name = name.replace("'", '')
                    name = name.replace(".", '')
                    name = name.replace('Nunu&Willump', 'Nunu')
                    self.champlist_save.append(name)
                    f.write(name + '\n')


    def convert_champlist_to_icon(self):
        for name in self.champlist_raw:
            name = name.replace(' ', '')
            name = name.replace("'", '')
            name = name.replace(".", '')
            name = name.replace('AurelionSol', 'Aurelion_Sol')
            name = name.replace('ChoGath', 'Cho%27Gath')
            name = name.replace('JarvanIV', 'Jarvan_IV')
            name = name.replace('KaiSa', 'Kai%27Sa')
            name = name.replace('KhaZix', 'Kha%27Zix')
            name = name.replace('KogMaw', 'Kog%27Maw')
            name = name.replace('LeeSin', 'Lee_Sin')
            name = name.replace('MasterYi', 'Master_Yi')
            name = name.replace('MissFortune', 'Miss_Fortune')
            name = name.replace('Nunu&Willump', 'Nunu_&_Willump')
            name = name.replace('RekSai', 'Rek%27Sai')
            name = name.replace('TahmKench', 'Tahm_Kench')
            name = name.replace('TwistedFate', 'Twisted_Fate')
            name = name.replace('VelKoz', 'Vel%27Koz')
            name = name.replace('XinZhao', 'Xin_Zhao')

            self.champlist_icon.append(name)


    """ NAME CONVERSION """

    @staticmethod
    def convert_to_save_name(name):
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