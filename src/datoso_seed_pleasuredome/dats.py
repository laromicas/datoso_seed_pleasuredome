"""PleasureDome Dat class to parse different types of dat files."""
import json
import logging
import re
from pathlib import Path

from datoso.configuration import config
from datoso.repositories.dat_file import ClrMameProDatFile, DatFile, DirMultiDatFile, XMLDatFile

# pylint: disable=attribute-defined-outside-init,unsupported-membership-test


def mame_dat_factory(file: str) -> DatFile | None:
    """Dat factory."""
    ext = Path(file).suffix
    if ext in ('.dat', '.xml'):
        return MameDat
    if Path.is_dir(file):
        return MameDirDat
    return None

def hbmame_dat_factory(file: str) -> DatFile | None:
    """Dat factory."""
    ext = Path(file).suffix
    if ext in ('.dat', '.xml'):
        return HomeBrewMameDat
    if Path.is_dir(file):
        return HomeBrewMameDirDat
    return None


def get_version(string: str) -> str | None:
    """Get the version from the dat file."""
    search = re.findall(r'0\.[0-9]*[\.[0-9]*]?', str(string))
    if search:
        return search[-1]
    return None


def remove_extra_spaces(string: str) -> str:
    """Remove extra spaces from the dat file."""
    return re.sub(' +', ' ', string)


class MameDirDat(DirMultiDatFile):
    """Mame Dir Dat class."""

    seed: str = 'pleasuredome'

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        self.company = None
        self.system = 'MAME'
        self.suffix = None
        self.prefix = self.system_type = 'Arcade'
        file_name = str(self.file)
        self.version = get_version(file_name)

        if 'Update' in file_name:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]


class MameDat(XMLDatFile):
    """Mame Dat class."""

    seed: str = 'pleasuredome'

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        self.company = 'MAME'
        self.suffix = None
        self.prefix = self.system_type = 'Arcade'
        file_name = str(self.file)
        self.version = self.header.get('version', get_version(file_name))

        if 'Update' in file_name:
            self.suffix = 'Update'
        else:
            try:
                self.name = remove_extra_spaces(self.name.replace(self.version, ''))
            except TypeError:
                print(self.name)
                print(self.version)
                print(self.__dict__['header'])
                raise
        if 'dir2dat' in file_name and 'dir2dat' not in self.name:
            self.name = f'{self.name} (dir2dat)'
        self.system = self.name

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]


class HomeBrewMameDirDat(MameDirDat):
    """HomeBrew Mame Dir Dat class."""

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        super().initial_parse()
        self.company = ''
        self.system = 'HBMAME'


class HomeBrewMameDat(MameDat):
    """HomeBrew Mame Dat class."""

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        super().initial_parse()
        self.company = 'HBMAME'



class RaineDat(MameDat):
    """HomeBrew Mame Dat class."""

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        super().initial_parse()
        self.company = 'Raine'

class PinballDat(XMLDatFile):
    """HomeBrew Mame Dat class."""

    allowed_systems = ['Future Pinball', 'Visual Pinball']

    def get_system(self) -> str:
        """Get the system from the dat file."""
        for system in self.allowed_systems:
            if system in self.name:
                return system
        return 'Pinball'

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        # Remove date from name
        self.name = self.name.split('(')[0].strip()
        self.company = None
        self.system = self.get_system()
        self.suffix = self.name

        self.overrides()

        if self.modifier or self.system_type:
            self.prefix = config.get('PREFIXES', self.modifier or self.system_type, fallback='Pinball')
        else:
            self.prefix = None

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]

class KawaksDat(MameDat):
    """HomeBrew Mame Dat class."""

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        super().initial_parse()
        self.company = 'Kawaks'


def fruit_machine_factory(file_name: str) -> DatFile | None:
    """Fruit Dat factory."""
    dat_class = DatFile.class_from_file(file_name)
    if dat_class == XMLDatFile:
        return FruitMachinesXMLDat
    if dat_class == ClrMameProDatFile:
        return FruitMachinesClrMameDat
    logging.error('Unknown Fruit Machine Dat file: %s', file_name)
    return None


class FruitMachinesXMLDat(XMLDatFile):
    """Fruit Machines Dat class."""

    def load_metadata_file(self) -> dict:
        """Load the metadata file."""
        file  = Path(self.file)
        metadata_file = file.parent / 'metadata.txt'
        metadata = {}
        if metadata_file.exists():
            with open(metadata_file, encoding='utf-8') as file:
                metadata = json.load(file)
        return metadata

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        name = self.name
        extra_data = self.load_metadata_file()

        name = name.split('(')[0].strip()
        self.suffix = get_suffix(self.file)

        self.company = 'Fruit'
        self.system = extra_data.get('folder', name)

        self.prefix = 'Arcade'

        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]

    def get_date(self) -> str:
        """Get the date from the dat file."""
        if self.file and '(' in str(self.file):
            file = str(self.file)
            self.date = file[file.find('(')+1:file.find(')')]
        return self.date


class FruitMachinesClrMameDat(ClrMameProDatFile):
    """Fruit Machines Dat class."""

    seed: str = 'pleasuredome'

    def load_metadata_file(self) -> dict:
        """Load the metadata file."""
        file = Path(self.file)
        file_name = file.parent / 'metadata.txt'
        metadata = {}
        if Path.exists(file_name):
            with open(file_name, encoding='utf-8') as file:
                metadata = json.load(file)
        return metadata

    def initial_parse(self) -> list:
        # pylint: disable=R0801
        """Parse the dat file."""
        name = self.name
        extra_data = self.load_metadata_file()
        # print(extra_data)
        # exit()

        name = name.split('(')[0].strip()
        self.suffix = get_suffix(self.file)

        self.company = 'Fruit'
        self.system = extra_data.get('folder', name)

        self.prefix = 'Arcade'
        return [self.prefix, self.company, self.system, self.suffix, self.get_date()]

    def get_date(self) -> str:
        """Get the date from the dat file."""
        if self.file and '(' in str(self.file):
            file = str(self.file)
            self.date = file[file.find('(')+1:file.find(')')]
        return self.date

def get_suffix(file_name: str) -> str:
    """Get the suffix from the dat file."""
    if 'Layouts' in str(file_name):
        return 'Layouts'
    elif 'MPU5 Hexfiles' in str(file_name):
        return 'MPU5 Hexfiles'
    elif 'Snapshots' in str(file_name):
        return 'Snapshots'
    elif 'Rollback' in str(file_name):
        if '2009' in str(file_name):
            return 'Rollback/2009'
        if '2018' in str(file_name):
            return 'Rollback/2018'
        return 'Rollback'
    elif 'SWP Machine Roms' in str(file_name):
        return 'SWP Machine Roms'
    return 'Roms'
