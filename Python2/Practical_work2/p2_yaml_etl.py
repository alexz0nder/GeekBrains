import yaml, pprint

data_dir = 'data'
data_file = 'file.yml'

# Data structure to write
#    currency:
#        - rubble
#        - dollar
#        - euro
#    current_number: 22
#    symbols:
#        rubble: "\u0420"
#        dollar: "\u003b"
#        euro: "\u20ac"
#        yen: '\u00A5'

data = {
    'currency': [
        'rubble',
        'dollar',
        'euro',
    ],
    'current_number': 22,
    'symbols': {
        'rubble': '\u0420',
        'dollar': '\u0024',
        'euro': '\u20ac',
        'yen': '\u00A5',
    }
}

with open(data_dir + '/' + data_file, 'w') as file:
    yaml.dump(data, file, Dumper=yaml.Dumper, default_flow_style=False, allow_unicode = True)

with open(data_dir + '/' + data_file, 'r') as file:
    printer = pprint.PrettyPrinter(indent=4)
    printer.pprint(
        yaml.load(file, Loader=yaml.Loader)
    )
