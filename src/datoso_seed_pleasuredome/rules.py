"""Rules for the PleasureDome seed."""
from datoso_seed_pleasuredome.dats import FruitMachinesXMLDat, HomeBrewMameDat, MameDat

rules = [
    {
        'name': 'PleasureDome DATs',
        '_class': HomeBrewMameDat,
        'seed': 'pleasuredome',
        'priority': 70,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'HBMAME',
            },
        ],
    },
    {
        'name': 'PleasureDome DATs',
        '_class': MameDat,
        'seed': 'pleasuredome',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'MAME',
            },
        ],
    },
    {
        'name': 'PleasureDome DATs',
        '_class': FruitMachinesXMLDat,
        'seed': 'pleasuredome',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'Fruit Machine',
            },
        ],
    },
    {
        'name': 'PleasureDome DATs',
        '_class': FruitMachinesXMLDat,
        'seed': 'pleasuredome',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'FruitMachine',
            },
        ],
    },
    {
        'name': 'PleasureDome DATs',
        '_class': FruitMachinesXMLDat,
        'seed': 'pleasuredome',
        'priority': 50,
        'rules': [
            {
                'key': 'name',
                'operator': 'contains',
                'value': 'SWP Machine',
            },
        ],
    },
]

def get_rules() -> list:
    """Get the rules."""
    return rules
