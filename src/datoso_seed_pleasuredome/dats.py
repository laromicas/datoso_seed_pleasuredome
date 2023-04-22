"""
    PleasureDome Dat class to parse different types of dat files.
"""
import os
import re
import json
from pathlib import Path

from datoso.repositories.dat import XMLDatFile, DirMultiDatFile
# pylint: disable=attribute-defined-outside-init,unsupported-membership-test


def mame_dat_factory(file: str):
    """ Dat factory. """
    ext = Path(file).suffix
    if ext in ('.dat', '.xml'):
        return MameDat
    if os.path.isdir(file):
        return MameDirDat
    return None


def get_version(string: str):
    """ Get the version from the dat file. """
    search = re.findall(r'0\.[0-9]*[\.[0-9]*]?', string)
    if search:
        return search[-1]
    return None


def remove_extra_spaces(string: str):
    """ Remove extra spaces from the dat file. """
    return re.sub(' +', ' ', string)


class MameDirDat(DirMultiDatFile):
    """ Mame Dir Dat class. """

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """

        self.company = None
        self.system = 'MAME'
        self.suffix = None
        self.preffix = 'Arcade'
        self.version = get_version(self.file)

        if 'Update' in self.file:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


class MameDat(XMLDatFile):
    """ Mame Dat class. """

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """

        self.company = None
        self.system = 'MAME'
        self.suffix = None
        self.preffix = 'Arcade'
        self.version = get_version(self.file)

        if 'Update' in self.file:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))
        if 'dir2dat' in self.file and 'dir2dat' not in self.name:
            self.name = f'{self.name} (dir2dat)'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


class HomeBrewMameDat(XMLDatFile):
    """ HomeBrew Mame Dat class. """

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """

        self.company = None
        self.system = 'HBMAME'
        self.suffix = None
        self.preffix = 'Arcade'
        self.version = get_version(self.file)

        if 'Update' in self.file:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))
        if 'dir2dat' in self.file and 'dir2dat' not in self.name:
            self.name = f'{self.name} (dir2dat)'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


class FruitMachinesDat(XMLDatFile):
    """ Fruit Machines Dat class. """

    def load_metadata_file(self):
        """ Load the metadata file. """
        basedir = Path(self.file).parents[0]
        filename = os.path.join(basedir, 'metadata.txt')
        if os.path.exists(filename):
            with open(filename, encoding='utf-8') as file:
                metadata = json.load(file)
        return metadata


    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """
        name = self.name
        extra_data = self.load_metadata_file()

        name = name.split('(')[0].strip()
        if 'Layouts' in self.file:
            self.suffix = 'Layouts'

        self.company = 'Fruit'
        self.system = extra_data['folder']

        self.preffix = 'Arcade'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self):
        """ Get the date from the dat file. """
        if self.file and '(' in self.file:
            file = str(self.file)
            self.date = file[file.find("(")+1:file.find(")")]
        return self.date
