from datoso.configuration import config


def seed_args(parser):
    parser.add_argument('-do', '--download', help='Download the specified sets', nargs='+',
                choices=['mame', 'hbmame', 'fruitmachines', 'demul', 'fbneo', 'kawaks', 'pinball', 'pinmame', 'raine'])

def post_parser(args):
    if getattr(args, 'download', None) is not None:
        config['PLEASUREDOME']['download'] = ','.join(args.download)

def init_config():
    if not config.has_section('PLEASUREDOME'):
        config['PLEASUREDOME'] = {
            'download': 'mame,hbmame,fruitmachines',
        }
