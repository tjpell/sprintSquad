import glob
import json
import os
import sys

def extract_Data(infile, output):
    """
    Input: file 
    Output: list of strings containing names and ages 
    Function extracts JSON blobs from lines of input file
    """
    lines = []
    with open(infile) as f:
        oldlines = f.readlines()
    if oldlines:
        for i in range(len(oldlines)):
            try:
                lines.append(json.loads(oldlines[i]))
            except ValueError: #catches non-json format
                pass
        lines = [l for l in lines if 'name' in l and 'prop' in l and 'age' in l['prop']] #keys exist
        lines = [l for l in lines if l.get('name') and l.get('prop').get('age')] #keys aren't null
        names = [l['name'] for l in lines]
        ages = [l['prop']['age'] for l in lines]
        for n,a in zip(names, ages):
            output.append(n + '\t' + str(a))
        
os.system('cd ../..')
os.system('pwd')
path = '/srv/runme/'
prefix = sys.argv[1]

# tmp = path + 'tmp/'
# if not os.path.exists(tmp):
#     os.mkdir(tmp)
# os.system('mv ' + path + prefix + '.txt ' + path + prefix + '.json')
# os.system('rm ' + path + prefix + '.txt')
# files = [filename for filename in os.listdir('.') if filename.startswith(prefix)]

files = glob.glob(path + prefix + '*')
print "files:" , files
output = []
for f in files:
    try:
        extract_Data(f, output)
    except ValueError:
        print "BAD FILE oops."

# move the prefix.txt out of temp
# os.system('mv ' + path + 'tmp/' + prefix + '.txt ' + path + prefix + '.txt')
# os.system('mv ' + 'tmp/' + prefix + '.txt ..')
# os.system('rm -rf ' + tmp)

outfile = path + '{}.txt'.format(prefix)
os.system('rm  ' + outfile)

with open(outfile, 'w') as f:
    f.write('\n'.join(output)+'\n')
