"""Fetch and download DAT files."""
import json
import logging
import os
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from typing import ClassVar
from urllib.parse import urljoin

import dateutil.parser

from datoso.configuration import config
from datoso.configuration.folder_helper import Folders
from datoso.helpers import FileUtils
from datoso.helpers.download import downloader
from datoso_seed_pleasuredome import __prefix__

# ruff: noqa: ERA001

# TODO(laromicas): Auto add sets from the website https://pleasuredome.github.io/pleasuredome/nonmame/index.html

MAME_URL = 'https://pleasuredome.github.io/pleasuredome/mame/index.html'

class MyHTMLParser(HTMLParser):
    """A custom HTML parser for parsing Pleasuredome HTML."""

    dats: list = None
    rootpath = None

    def handle_starttag(self, tag: str, attrs: list) -> None:
        """Handle the start tag of an HTML element, capture the zip hrefs."""
        if self.dats is None:
            self.dats = []
        if tag == 'a':
            taga = dict(attrs)
            if 'href' in taga:
                href = taga['href']
                if href.endswith('.zip'):
                    self.dats.append(urljoin(self.rootpath, href).replace(' ', '%20'))


class PDSET(Enum):
    """Pleasuredome DAT Enum."""

    MAME: ClassVar = {
            'url': 'https://pleasuredome.github.io/pleasuredome/mame/index.html',
            'configVar': 'mame',
            'actions': [
                'extract_mame_dats',
            ],
        }
    Reference: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/mame/mame-reference-sets/index.html',
        'configVar': 'mame_reference',
    }
    HBMAME: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/hbmame/index.html',
        'configVar': 'hbmame',
        'actions': [
            'extract_fruit_hbmame_dats',
        ],
    }
    FruitMachines: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/fruitmachines/index.html',
        'configVar': 'fruitmachines',
        'actions': [
            'write_metadata_fruit',
            'extract_fruit_hbmame_dats',
        ],
    }
    Demul: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/demul/index.html',
        'configVar': 'demul',
    }
    FinalBurnNeo: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/fbneo/index.html',
        'configVar': 'fbneo',
    }
    Kawaks: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/kawaks/index.html',
        'configVar': 'kawaks',
        'actions': [
            'extract_fruit_hbmame_dats',
        ],
    }
    Pinball: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/pinball/index.html',
        'configVar': 'pinball',
    }
    PinMAME: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/pinmame/index.html',
        'configVar': 'pinmame',
    }
    Raine: ClassVar = {
        'url': 'https://pleasuredome.github.io/pleasuredome/nonmame/raine/index.html',
        'configVar': 'raine',
        'actions': [
            'extract_fruit_hbmame_dats',
        ],
    }

class PleasureDomeHelper:
    """Helper class for Pleasuredome."""

    def __init__(self, folder_helper: Folders) -> None:
        """Initialize PleasureDomeHelper."""
        self.folder_helper = folder_helper

    def get_dat_links(self, name: str, mame_url: str) -> list:
        """Get DAT links from Pleasuredome."""
        print(f'Fetching {name} DAT files')
        if not mame_url.startswith(('http', 'https')):
            msg = 'Invalid URL'
            raise ValueError(msg)
        red = urllib.request.urlopen(mame_url) # noqa: S310
        pleasurehtml = red.read()

        parser = MyHTMLParser()
        parser.dats = []
        parser.rootpath = mame_url
        parser.folder_helper = self.folder_helper
        parser.feed(str(pleasurehtml))
        return parser.dats

    def download_dat(self, href: str, folder: str) -> None:
        """Download a DAT file."""
        filename = Path(href).name.replace('%20', ' ')
        downloader(url=href, destination=self.folder_helper.dats / folder / filename, reporthook=None)

    def extract_date(self, filename: str) -> datetime:
        """Extract date from filename."""
        datetext = Path(filename).stem.replace('%20', ' ').split('-')[1]
        return dateutil.parser.parse(datetext)

    def write_metadata_fruit(self, name: str, files: list) -> None:
        """Write metadata for FruitMachines."""
        path = self.folder_helper.dats / name
        for file in files:
            if 'FruitMachines' in file and file.endswith('.zip'):
                date = self.extract_date(file)
            with open(path / 'metadata.txt', 'w') as f:
                metadata = {
                    'name': 'FruitMachines',
                    'date': date.strftime('%Y-%m-%d'),
                    'zipfile': file,
                    'folder': Path(file).stem,
                }
                f.write(json.dumps(metadata, indent=4))

    def backup_file(self, path: str, file: str) -> None:
        """Backup a file."""
        path.mkdir(parents=True, exist_ok=True)
        FileUtils.move(file, path)

    def extract_fruit_hbmame_dats(self, name: str, files: str) -> None:
        """Extract FruitMachines and HBMAME DATs."""
        path = self.folder_helper.dats / name
        for file in files:
            filepath = path / file
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(path)
            # filepath.unlink()
            self.backup_file(self.folder_helper.backup /name, filepath)

    def extract_mame_dats(self, name: str, files: list) -> None:
        """Extract MAME DATs."""
        path = self.folder_helper.dats / name
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
                    # filepath.unlink()
                    self.backup_file(self.folder_helper.backup /name, filepath)
                except zipfile.BadZipFile:
                    logging.exception('Error extracting %s', filename)
            else:
                try:
                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                        zip_ref.extractall(path)
                    # filepath.unlink()
                    self.backup_file(self.folder_helper.backup /name, filepath)
                except zipfile.BadZipFile:
                    logging.exception('Error extracting %s', filename)

    def download_dats(self) -> None:
        """Download DAT files."""
        sets_to_download = config.get('PLEASUREDOME', 'download', fallback='mame,hbmame,fruitmachines').split(',')
        for pdset in PDSET:
            if pdset.name.lower() not in sets_to_download:
                continue
            name = pdset.name
            url = pdset.value['url']
            links = self.get_dat_links(name, url)

            print(f'Downloading {name} DAT files')
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [
                    executor.submit(self.download_dat, href, name) for href in links
                ]
                for future in futures:
                    future.result()

            path = self.folder_helper.dats / name
            files = os.listdir(path)
            for action in pdset.value.get('actions', []):
                func = getattr(self, action)
                func(name, files)


def fetch() -> None:
    """Fetch and download DAT files."""
    folder_helper = Folders(seed=__prefix__, extras=[x.name for x in PDSET])
    folder_helper.clean_dats()
    folder_helper.create_all()
    pleasure_dome = PleasureDomeHelper(folder_helper)
    pleasure_dome.download_dats()
