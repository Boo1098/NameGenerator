from os import listdir
from os.path import isfile, join
import whois

# Warning if you use all years it will take a LONG time
START_YEAR = 1900
END_YEAR = 1910

NAME_PATH = r'names/'
files = [f for f in listdir(NAME_PATH) if isfile(join(NAME_PATH, f)) and START_YEAR < int(f[3:7]) < END_YEAR]
print(files)

names = []
for filename in files:
    print('Starting to read {}'.format(filename))
    with open((NAME_PATH + '{}').format(filename)) as f:
        for line in f:
            name = line.split(',')[0]
            if name not in names:
                names.append(name)

# Filter names that don't have an a in them
new_names = []
for name in names:
    split = name.split('a')
    if len(split) != 1:
        split = [split[0], 'a'.join(split[1:len(split)])]
        new_names.append(split)
names = new_names

tlds = []
with open(r'tlds.txt') as f:
    for line in f:
        tlds.append(line.strip())

# Filter names that end with tld
new_names = []
for name in names:
    for tld in tlds:
        if name[1].endswith(tld):
            if len(tld) != len(name[1]):
                new_names.append([name[0], name[1][:-len(tld)], tld])
names = new_names

# TODO
# Filter taken domains
# new_names = []
# for name in names:
#     url = '{}.{}'.format(name[1], name[2])
#     w = whois.whois(url)
#     if w['status'] is None:
#         new_names.append(name)

for name in names:
    print('{}@{}.{}'.format(name[0], name[1], name[2]))
