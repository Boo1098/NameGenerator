from os import listdir
from os.path import isfile, join
import whois

# Warning if you use all years it will take a LONG time
START_YEAR = 2018
END_YEAR = 2020

NAME_PATH = r'names/'
TLD_FILE = r'tlds.txt'


def print_names(raw_names):
    for raw_name in raw_names:
        print(format_name(raw_name))


def format_name(raw_name):
    return '{}@{}.{}'.format(raw_name[0], raw_name[1], raw_name[2])


files = [f for f in listdir(NAME_PATH) if isfile(join(NAME_PATH, f)) and START_YEAR <= int(f[3:7]) < END_YEAR]
print(files)

names = []
for filename in files:
    print('Starting to read {}'.format(filename))
    with open((NAME_PATH + '{}').format(filename)) as f:
        for line in f:
            name = line.split(',')[0]
            if name not in names:
                names.append(name)
print('{} names parsed'.format(len(names)))

tlds = []
with open(TLD_FILE) as f:
    for line in f:
        tlds.append(line.strip())
print('{} tlds parsed'.format(len(tlds)))

# Filter names that don't have an a in them
new_names = []
for name in names:
    split = name.split('a')
    if len(split) != 1:
        split = [split[0], 'a'.join(split[1:len(split)])]
        new_names.append(split)
names = new_names

# Filter names that end with tld
new_names = []
for name in names:
    for tld in tlds:
        if name[1].endswith(tld):
            if len(tld) != len(name[1]):  # Filter names where the domain would be ".tld"
                new_names.append([name[0], name[1][:-len(tld)], tld])
names = new_names

# TODO
# Filter taken domains
# new_names = []
# count = 0
# for name in names:
#     count += 1
#     url = '{}.{}'.format(name[1], name[2])
#     if len(name[1]) >= 3:
#         try:
#             w = whois.whois(url)
#         except:
#             print('whois failed for {}'.format(format_name(name)))
#         try:
#             if w['status'] is None:
#                 new_names.append(name)
#         except:
#             print('oops')
#
#     if count % 10 == 0:
#         print('{}/{}'.format(count, len(names)))
# names = new_names

print_names(names)

with open('names.txt', 'w') as f:
    for name in names:
        f.write('%s\n' % format_name(name))
