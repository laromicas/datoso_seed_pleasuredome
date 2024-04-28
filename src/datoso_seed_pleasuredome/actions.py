from datoso_seed_pleasuredome.dats import HomeBrewMameDat, fruit_machine_factory, mame_dat_factory

# ruff: noqa: ERA001

actions = {
    '{dat_origin}/FruitMachines': [
        {
            'action': 'LoadDatFile',
            '_factory': fruit_machine_factory,
        },
        {
            'action': 'DeleteOld',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
    '{dat_origin}/HBMAME': [
        {
            'action': 'LoadDatFile',
            '_class': HomeBrewMameDat,
        },
        {
            'action': 'DeleteOld',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
    '{dat_origin}/MAME': [
        {
            'action': 'LoadDatFile',
            '_factory': mame_dat_factory,
        },
        {
            'action': 'DeleteOld',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
    # '{dat_origin}/Reference': [
    #     {
    #         'action': 'LoadDatFile',
    #         '_factory': mame_dat_factory
    #     },
    #     {
    #         'action': 'DeleteOld'
    #     },
    #     {
    #         'action': 'Copy',
    #         'folder': '{dat_destination}'
    #     },
    #     {
    #         'action': 'SaveToDatabase'
    #     }
    # ]
}

def get_actions():
    return actions
