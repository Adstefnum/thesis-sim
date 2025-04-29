#!/usr/bin/python

from os import path, scandir
from sys import argv



dt = float(argv[1])
folder = './postProcessing'
t = 0

if path.isfile(folder + f'/processed/{t}/line.xy'):
    files_available = True
    print(files_available)
else:
    files_available = False 
ign_t = []
c_criteria = 0.5
y_max = 7.65

while files_available:
    try:
        c_file = open(folder + f'/processed/{t}/line.xy')
        burning = True
        while burning:
            if len(ign_t) > 0:
                y0 = ign_t[-1][0]
            else:
                y0 = 0.0
            y = -999999
            while y <= y0:
                try:
                    a = c_file.readline()
                    (y, c) = a.split()
                    y = float(y)
                    c = float(c)
                except ValueError:
                    burning = False
                    print('EEEE', t)
                    break
            if c >= c_criteria and y > -999999:
                # print(y, t, end='\t')
                ign_t.append((y, t))
            else:
                burning = False
        c_file.close()
        # print('Rastas laikas ', t)
        t = round(t + dt, 7)

    except OSError:
        files_available = False

    if len(ign_t) > 0:
        if ign_t[-1][0] >= y_max:
            burning = False
            files_available = False
            break

processed_file = folder + f'/processed_ignitions_{dt}.txt'
processed_file_2 = folder + f'/processed_reversed_ignitions_{dt}.txt'

if len(ign_t) > 2:
    out_file = open(processed_file, 'w')
    out_file_2 = open(processed_file_2, 'w')
    for ign_pair in ign_t:
        out_file.write('{}\t{}\n'.format(*ign_pair))
        out_file_2.write('{}\t{}\n'.format(ign_pair[1], ign_pair[0]))
    out_file.close()
    out_file_2.close()

    pruned = []

    with open(processed_file) as ign_file:
        pos, time = ign_file.readline().split()
        pos = float(pos)
        time = float(time)
        for line in ign_file:
            posN, timeN = line.split()
            posN = float(posN)
            timeN = float(timeN)
            if timeN != time:
                pruned.append((pos, time))
            pos = posN
            time = timeN

    for i in range(1, len(pruned) - 1):
        print(
            pruned[i][0],
            (pruned[i + 1][0] - pruned[i - 1][0])
            / (pruned[i + 1][1] - pruned[i - 1][1]),
        )

    out_file = open(processed_file.replace('ignitions', 'velocity'), 'w')
    for i in range(1, len(pruned) - 1):
        out_file.write(
            f'{pruned[i][0]}\t{(pruned[i + 1][0] - pruned[i - 1][0]) / (pruned[i + 1][1] - pruned[i - 1][1])}\n'
        )
    out_file.close()
