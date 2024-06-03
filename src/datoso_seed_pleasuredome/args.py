"""Argument parser for Pleasuredome seed."""
from argparse import ArgumentParser, Namespace

from datoso.configuration import config


def seed_args(parser: ArgumentParser) -> ArgumentParser:
    """Add seed arguments to the parser."""
    parser.add_argument('-do', '--download', help='Download the specified sets', nargs='+',
                choices=['mame', 'hbmame', 'fruitmachines', 'demul', 'fbneo', 'kawaks', 'pinball', 'pinmame', 'raine'])
    return parser

def post_parser(args: Namespace) -> None:
    """Post parser actions."""
    if getattr(args, 'download', None) is not None:
        config['PLEASUREDOME']['download'] = ','.join(args.download)

def init_config() -> None:
    """Initialize the configuration."""
    if not config.has_section('PLEASUREDOME'):
        config['PLEASUREDOME'] = {
            'download': 'mame,hbmame,fruitmachines',
        }
