import glob
import json
import os

def extract_Data(infile, outfile):
    with open(infile) as f:
        lines = f.readlines()
    lines = [json.loads(l) for l in lines]
    lines = [l for l in lines if l.get('prop').get('age') and l.get('name')]
    names = [l['name'] for l in lines]
    ages = [l['prop']['age'] for l in lines]
    with open(outfile, 'w') as f:
        for n, a in zip(names, ages):
            print n + '\t' + str(a) + '\n'
            f.write(n + '\t' + str(a) + '\n')

prefix = 'prefix'
path = '../../srv/runme/'
files = glob.glob(path + '*prefix*')

# files = [filename for filename in os.listdir('.') if filename.startswith("prefix")]
print "files:" , files
for f in files:
    try:
        extract_Data(f, path + '{}.txt'.format(prefix))
    except ValueError:
        pass
