#!/usr/bin/python

from os import makedirs, path, scandir

folder = 'postProcessing'

locs = [f.name for f in scandir(folder) if f.is_dir() and 'line' in f.name]
print(locs)

try:
    times = [f.name for f in scandir(folder + '/' + locs[-1]) if f.is_dir()]
except IndexError:
    times = ()

if len(times) == 0:
    times = ['']

if len(locs) > 0:
    if not path.isfile(folder + '/{}/{}/line.xy'.format(locs[0], times[0])):
        locs2 = [f.name for f in scandir(folder + '/' + locs[0]) if f.is_dir()]
        try:
            times = [
                f.name
                for f in scandir(folder + '/' + locs[0] + '/' + locs2[0])
                if f.is_dir()
            ]
        except IndexError:
            times = ()
    elif 'locs2' in locals():
        del locs2

if path.isdir(folder + '/processed'):
    times_processed = [f.name for f in scandir(folder + '/processed') if f.is_dir()]
else:
    times_processed = ()

i = 0
for time in times:
    if time in times_processed:
        continue
    if i < 18:
        print(time, end=' ')
        i += 1
    else:
        print(time, '\n\t', end=' ')
        i = 0
    result = {}
    data = []
    for loc in locs:
        if 'locs2' in locals():
            loc += '/' + locs2[0]
        with open(folder + '/{}/{}/line.xy'.format(loc, time)) as myfile:
            data.append(myfile.readlines())

    makedirs(folder + '/processed/{}'.format(time), exist_ok=True)
    output = open(folder + '/processed/{}/line.xy'.format(time), 'w')

    for singleGraphFile in data:
        for line in singleGraphFile:
            if line.startswith('#') or len(line) == 1:
                continue
            (h, c) = line.split()
            c = float(c)
            if h in result.keys():
                if c > result[h]:
                    result[h] = c
            else:
                result[h] = c
    for h in sorted(result.keys()):
        output.write('{}\t{}\n'.format(h, result[h]))
    output.close()
