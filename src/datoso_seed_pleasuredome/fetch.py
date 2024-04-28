import json
import logging
import os
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import dateutil.parser

from datoso.configuration.folder_helper import Folders
from datoso.helpers.download import downloader
from datoso_seed_pleasuredome import __prefix__

# ruff: noqa: ERA001

MAME_URL = 'https://pleasuredome.github.io/pleasuredome/mame/index.html'
SETS = {
    'MAME': {
        'url': 'https://pleasuredome.github.io/pleasuredome/mame/index.html',
    },
    # 'Reference': {
    #     'url': 'https://pleasuredome.github.io/pleasuredome/mame-reference-sets/index.html'
    # },
    'HBMAME': {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/hbmame/index.html',
    },
    'FruitMachines': {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/fruitmachines/index.html',
    },
}


class MyHTMLParser(HTMLParser):
    dats: list = None
    rootpath = None

    def handle_starttag(self, tag, attrs):
        if self.dats is None:
            self.dats = []
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
        downloader(url=href, destination=folder_helper.dats / folder / filename, reporthook=None)

    def extract_date(filename):
        datetext = Path(filename).stem.replace('%20', ' ').split('-')[1]
        return dateutil.parser.parse(datetext)

    def write_metadata_fruit(path, files):
        for file in files:
            if 'FruitMachines' in file and file.endswith('.zip'):
                date = extract_date(file)
            with open(path / 'metadata.txt', 'w') as f:
                metadata = {
                    'name': 'FruitMachines',
                    'date': date.strftime('%Y-%m-%d'),
                    'zipfile': file,
                    'folder': Path(file).stem,
                }
                f.write(json.dumps(metadata, indent=4))

    def extract_fruit_hbmame_dats(path, files):
        for file in files:
            filepath = path / file
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(path)
            filepath.unlink()

    def extract_mame_dats(path, files):
        for file in files:
            filepath = path / file
            filename = str(filepath)
            if ('Software List' in filename and 'dir2dat' not in filename) \
                or 'EXTRA' in filename:
                new_path = path / filepath.stem
                new_path.mkdir(parents=True, exist_ok=True)
                try:
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        zip_ref.extractall(new_path)
                    filepath.unlink()
                except zipfile.BadZipFile:
                    logging.exception('Error extracting %s', filename)
            else:
                try:
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        zip_ref.extractall(path)
                    filepath.unlink()
                except zipfile.BadZipFile:
                    logging.exception('Error extracting %s', filename)

    for name, sets in SETS.items():
        if name == 'Reference': # TODO(laromicas): allow reference sets by configuration
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

        path = folder_helper.dats / name
        files = os.listdir(path)
        if name in ('FruitMachines'):
            write_metadata_fruit(path, files)
        if name in ('FruitMachines', 'HBMAME'):
            extract_fruit_hbmame_dats(path, files)
        if name in ('MAME'):
            extract_mame_dats(path, files)



def fetch():
    folder_helper = Folders(seed=__prefix__, extras=SETS.keys())
    folder_helper.clean_dats()
    folder_helper.create_all()
    download_dats(folder_helper)
