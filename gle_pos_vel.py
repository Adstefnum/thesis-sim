#!/usr/bin/python

from glob import glob
from os import path, scandir, remove
from subprocess import run 
from tempfile import NamedTemporaryFile

processed_files = [
    processed_file
    for processed_file in glob('./postProcessing/processed_ignitions_*.txt')
]

print(processed_files)

colors = [
    'black',
    'red',
    'green',
    'blue',
    'orange',
    'magenta',
    'lime',
    'cyan',
    'yellow',
    'Brown',
    'skyblue',
    'olive',
    'tomato',
    '#e998af',
    '#98c4e9',
    '#e9be98',
    '#d8e998',
    '#9be998',
    '#98e9d2',
    '#aa98e9',
    'grey',
]

keys = {}
for processed_file in processed_files:
    key = processed_file.replace('./postProcessing/processed_ignitions_', '-')
    key = key.replace('.txt', '')
    print(key)
    parts = key.split('-')
    if len(parts) > 1 and len(processed_files) > 1:
        for part in parts:
            common = True
            for file_again in processed_files:
                if part not in file_again:
                    common = False
            if common:
                print(part)
                key = key.replace(part, '')
    print(key)
    while '--' in key:
        key = key.replace('--', '-')
    if len(key) > 1 and key[0] == '-':
        key = key[1:]
    if len(key) > 1 and key[-1] == '-':
        key = key[:-1]
    keys[processed_file] = key

print(keys)

gle_header = 'size 18 10\nbegin graph\n\tscale auto\n'
gle_header += '\taxis grid\n\tticks lstyle 2 color gray\n'
gle_footer = '\t!exp\n\tkey pos br\n'
gle_footer += '\txtitle "Height, m"\n\tytitle "Arrival time, s"\nend graph'
gle = gle_header

def sanitize(s):
    return s.replace('//', '/').replace('{', '').replace('}', '')

for file_nr, processed_file in enumerate(processed_files):
    sanitized_file = sanitize(processed_file)
    
    sanitized_key = keys[processed_file].split('_')[1]
    gle += f'\tdata {sanitized_file}\n\td{file_nr + 1} color {colors[file_nr]} key {sanitized_key} line\n'

gle += gle_footer

exp_nr = len(processed_files) + 1

with NamedTemporaryFile(mode='w', dir='.', delete=False) as temp:
    temp_name = temp.name
    if path.isfile('exp/pos.txt'):
        temp.write(gle.replace('!exp', f'data exp/pos.txt\n\td{exp_nr} marker circle'))
    else:
        temp.write(gle)
    # run(['gle', '-d', 'png', '-dpi', '200', '-o', 'pos.png', temp_name])
# remove(temp_name)

# print(gle)
gle = gle.replace('ignitions', 'velocity')
print(gle)

with NamedTemporaryFile(mode='w', dir='.', delete=False) as temp:
    temp_name = temp.name
    gle = gle.replace('Arrival time, s', 'Velocity, m/s')
    gle = gle.replace('br', 'tr')
    if path.isfile('exp/vel.txt'):
        temp.write(gle.replace('!exp', f'data exp/vel.txt\n\td{exp_nr} marker circle'))
    else:
        temp.write(gle)
    # run(['gle', '-d', 'png', '-dpi', '200', '-o', 'vel.png', temp_name])
    # run(['gle', '-o', 'vel.eps', temp_name])
# remove(temp_name)
