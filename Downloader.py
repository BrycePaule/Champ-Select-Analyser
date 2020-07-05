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


    """ SCRAPING """

    def scrapeChamplist(self):
        print('Scraping champlist')

        champs_url = 'https://na.leagueoflegends.com/en-us/champions/'

        uClient = uReq(champs_url)
        page_html = uClient.read()
        uClient.close()

        page = BeautifulSoup(page_html, 'html.parser')
        names = page.select('.style__Name-sc-12h96bu-2')
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


    def scrapeSplashes(self, champlist, download_bool=False):
        for name in champlist:
            if download_bool:
                link = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/' + name + '_0.jpg'

                name = self.editNameForSave(name)
                print('Downloading splash: ' + name)

                urllib.request.urlretrieve(link, 'Splashes_Raw/' + name + '.bmp')
            else:
                name = self.editNameForSave(name)
                print('Fixing splash: ' + name)

            splash = Image.open(self.splash_path + name + '.bmp')

            splash = self.IEdit.faceCover(name, splash)
            splash = self.IEdit.fixSplashes(name, splash)
            splash = self.IEdit.scaleSplash(name, splash)
            splash.save('Splashes/' + name + '.bmp')

            splash = ImageOps.mirror(splash)
            splash.save('Splashes/' + name + '_inverted.bmp')


    def scrapeIcons(self, champlist, download_bool=False):
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

                name = self.editNameForSave(name)

                print('Downloading icon: ' + name)
                urllib.request.urlretrieve(image_url, 'Icons_Raw/' + name + '.bmp')
            else:
                name = self.editNameForSave(name)
                print('Fixing icon: ' + name)

            icon = Image.open(self.icon_path + name + '.bmp')

            icon = self.IEdit.fixIcons(name, icon)
            icon = self.IEdit.scaleIcon(name, icon)
            icon.save('Icons/' + name + '.bmp')

            icon = ImageOps.mirror(icon)
            icon.save('Icons/' + name + '_inverted.bmp')


    """ CHAMPLIST """

    def fixAndExportChamplist(self, champlist):
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


    def fixChamplistForIconDownload(self, champlist):
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


    def editNameForSave(self, name):
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