"""Actions for the pleasuredome seed."""
from datoso_seed_pleasuredome.dats import (
        KawaksDat,
        RaineDat,
        fruit_machine_factory,
        hbmame_dat_factory,
        mame_dat_factory,
    )

# ruff: noqa: ERA001

actions = {
    '{dat_origin}/FruitMachines': [
        {
            'action': 'LoadDatFile',
            '_factory': fruit_machine_factory,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
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
            '_factory': hbmame_dat_factory,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
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
            'folder': '{dat_destination}',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
    '{dat_origin}/Raine': [
        {
            'action': 'LoadDatFile',
            '_class': RaineDat,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
    '{dat_origin}/Kawaks': [
        {
            'action': 'LoadDatFile',
            '_class': KawaksDat,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
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
    # ],
}

def get_actions() -> dict:
    """Get the actions dictionary."""
    return actions
