from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import urllib.request
import zipfile
from urllib.parse import urljoin
import dateutil.parser
from datoso.helpers import downloader
from datoso.configuration.folder_helper import Folders
from datoso_seed_pleasuredome import __preffix__

MAME_URL = 'https://pleasuredome.github.io/pleasuredome/mame/index.html'
SETS = {
    'MAME': {
        'url': 'https://pleasuredome.github.io/pleasuredome/mame/index.html'
    },
    # 'Reference': {
    #     'url': 'https://pleasuredome.github.io/pleasuredome/mame-reference-sets/index.html'
    # },
    'HBMAME': {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/hbmame/index.html'
    },
    'FruitMachines': {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/fruitmachines/index.html'
    },
}


class MyHTMLParser(HTMLParser):
    dats = []
    rootpath = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            taga = dict(attrs)
            if 'href' in taga:
                href = taga['href']
                if href.endswith('.zip'):
                    self.dats.append(urljoin(self.rootpath, href).replace(' ', '%20'))


def download_dats(folder_helper):
    def get_dat_links(name, mame_url):
        # get mame dats
        print(f'Fetching {name} DAT files')
        red = urllib.request.urlopen(mame_url)
        pleasurehtml = red.read()

        parser = MyHTMLParser()
        parser.dats = []
        parser.rootpath = mame_url
        parser.folder_helper = folder_helper
        parser.feed(str(pleasurehtml))
        return parser.dats

    def download_dat(href, folder):
        filename = Path(href).name.replace('%20', ' ')
        downloader(url=href, destination=os.path.join(folder_helper.dats, folder, filename), reporthook=None)

    def extract_date(filename):
        datetext = Path(filename).stem.replace('%20', ' ').split('-')[1]
        date = dateutil.parser.parse(datetext)
        return date

    for name, sets in SETS.items():
        if name == 'Reference': #TODO: allow reference sets by configuration
            continue
        url = sets['url']
        links = get_dat_links(name, url)

        print(f'Downloading {name} DAT files')
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(download_dat, href, name) for href in links
            ]
            for future in futures:
                future.result()

        path = os.path.join(folder_helper.dats, name)
        files = os.listdir(path)
        if name in ('FruitMachines'):
            for file in files:
                if 'FruitMachines' in file and file.endswith('.zip'):
                    date = extract_date(file)
                with open(os.path.join(path, 'metadata.txt'), 'w') as f:
                    metadata = {
                        'name': 'FruitMachines',
                        'date': date.strftime('%Y-%m-%d'),
                        'zipfile': file,
                        'folder': Path(file).stem,
                    }
                    f.write(json.dumps(metadata, indent=4))
        if name in ('FruitMachines', 'HBMAME'):
            for file in files:
                file = os.path.join(path, file)
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(path)
                os.remove(file)
        if name in ('MAME'):
            for file in files:
                file = os.path.join(path, file)
                if ('Software List' in file and 'dir2dat' not in file) \
                    or 'EXTRA' in file:
                    new_path = os.path.join(path, Path(file).stem)
                    os.makedirs(new_path, exist_ok=True)
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(new_path)
                    os.remove(file)
                else:
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(path)
                    os.remove(file)


def fetch():
    folder_helper = Folders(seed=__preffix__, extras=SETS.keys())
    folder_helper.clean_dats()
    folder_helper.create_all()
    download_dats(folder_helper)
