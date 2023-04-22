from datoso_seed_pleasuredome.dats import mame_dat_factory

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_factory': mame_dat_factory
        },
        {
            'action': 'DeleteOld'
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}'
        },
        {
            'action': 'SaveToDatabase'
        }
    ]
}

def get_actions():
    return actions