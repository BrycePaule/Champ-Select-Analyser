import os
import urllib.request
import Utils

from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq


class Scraper:

    """
    Scrapes champion list, splash arts and icons from the web, saving them
    locally.

    """

    def __init__(self):
        self.champlist_path = Utils.champlist_filepath
        self.champlist = []

        self.init_directories()


    def scrape_champlist(self):
        uClient = uReq('https://na.leagueoflegends.com/en-us/champions/')
        page_html = uClient.read()
        uClient.close()

        page = BeautifulSoup(page_html, 'html.parser')
        names = page.select('.sc-ce9b75fd-0')

        champlist = [name.get_text() for name in names]
        champlist = [self.parse_champ_name(name) for name in champlist]

        # Save locally
        if os.path.exists(self.champlist_path):
            os.remove(self.champlist_path)

        with open(self.champlist_path, 'x') as f:
            for name in champlist:
                self.champlist.append(name)
                f.write(name + '\n')

    def scrape_champ_splashes(self, champ_name, force_scrape = False):
        if not force_scrape and os.path.isfile(f'./Assets/Splashes_Raw/{champ_name}.bmp'):
            return

        champ_name_adjusted = self.manual_scrape_name_override(champ_name)
        url = f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ_name_adjusted}_0.jpg'
        save_path = f'./Assets/Splashes_Raw/{champ_name}.bmp'

        # print("Scraping splash: ", champ_name)
        urllib.request.urlretrieve(url, save_path)

    def scrape_champ_icons(self, champ_name, force_scrape = False):
        if not force_scrape and os.path.isfile(f'./Assets/Icons_Raw/{champ_name}.bmp'):
            return

        champ_name_adjusted = self.manual_scrape_name_override(champ_name)
        url = f'https://opgg-static.akamaized.net/meta/images/lol/latest/champion/{champ_name_adjusted}.png'
        save_path = f'./Assets/Icons_Raw/{champ_name}.bmp'

        # print("Scraping icon: ", champ_name)
        urllib.request.urlretrieve(url, save_path)

    @staticmethod
    def init_directories():
        os.makedirs('./Assets/Splashes_Raw/', exist_ok = True)
        os.makedirs('./Assets/Icons_Raw/', exist_ok = True)

    @staticmethod
    def manual_scrape_name_override(name):
        return name.replace("Wukong", 'MonkeyKing')

    @staticmethod
    def parse_champ_name(name):
        name = name.replace('\n', '')
        name = name.replace('%27', '')
        name = name.replace('_', '')
        name = name.replace(' ', '')
        name = name.replace("'", '')
        name = name.replace(".", '')
        name = name.replace('BelVeth', 'Belveth')
        name = name.replace("ChoGath", 'Chogath')
        name = name.replace('KaiSa', 'Kaisa')
        name = name.replace('KhaZix', 'Khazix')
        name = name.replace('LeBlanc', 'Leblanc')
        name = name.replace("MonkeyKing", 'Wukong')
        name = name.replace('Nunu&Willump', 'Nunu')
        name = name.replace('RenataGlasc', 'Renata')
        name = name.replace("VelKoz", 'Velkoz')
        return urllib.parse.quote(name)