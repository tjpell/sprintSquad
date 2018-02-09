import glob
import json
import os

def extract_Data(infile, outfile):
    with open(infile) as f:
        lines = f.readlines()
    lines = [json.loads(l) for l in lines]
    lines = [l for l in lines if 'name' in l and 'prop' in l and 'age' in l['prop']] #keys exist
    lines = [l for l in lines if l.get('name') and l.get('prop').get('age')] #keys aren't null
    names = [l['name'] for l in lines]
    ages = [l['prop']['age'] for l in lines]
    with open(outfile, 'a+') as f:
        for n,a in zip(names, ages):
            f.write(n + '\t' + str(a) + '\n')

os.system('cd ../..')
os.system('pwd')

prefix = sys.argv[1]
path = '/srv/runme/'

# os.system('mv ' + path + prefix + '.txt ' + path + prefix + '.json')
#
# os.system('rm ' + path + prefix + '.txt')

files = glob.glob(path + prefix + '*')

# files = [filename for filename in os.listdir('.') if filename.startswith(prefix)]
print "files:" , files

for f in files:
    try:
        extract_Data(f, 'tmp/' + path + '{}.txt'.format(prefix))
    except ValueError: #catches non-json files
        print "we fucked up"
        pass
    
os.system('mv tmp/' + path + prefix + '.txt ' + path + prefix + '.txt')
