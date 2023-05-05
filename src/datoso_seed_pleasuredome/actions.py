from datoso_seed_pleasuredome.dats import FruitMachinesDat, HomeBrewMameDat, mame_dat_factory

actions = {
    '{dat_origin}/FruitMachines': [
        {
            'action': 'LoadDatFile',
            '_class': FruitMachinesDat
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
    ],
    '{dat_origin}/HBMAME': [
        {
            'action': 'LoadDatFile',
            '_class': HomeBrewMameDat
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
    ],
    '{dat_origin}/MAME': [
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