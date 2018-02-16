import glob
import json
import os
import sys

def extract_Data(infile, outlist):
    """
    Infile: file of JSON blobs to be processed
    Output: list of strings containing names and ages extracted from properly formatted JSON blobs
    """

    json_lines = []
    with open(infile) as f:
        input_lines = f.readlines()
    if input_lines:
        for i in range(len(input_lines)):
            try:
                json_lines.append(json.loads(input_lines[i]))
            except ValueError:  # catches non-json formatted lines
                pass  # should print an error here

        # we should split out the conditionals to create each line one at a time so that our output is correct
        key_lines = [l for l in json_lines if 'name' in l and 'prop' in l and 'age' in l['prop']]  # keys exist
        lines = [l for l in key_lines if l.get('name') and l.get('prop').get('age')]  # keys aren't null
        names = [l['name'] for l in lines]
        ages = [l['prop']['age'] for l in lines]
        for n, a in zip(names, ages):
            outlist.append(n + '\t' + str(a))


if __name__ == "__main__":
    os.system('cd ../..')
    os.system('pwd')
    path = '/srv/runme/'
    prefix = sys.argv[1]

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

    outfile = path + '{}.txt'.format(prefix)
    os.system('rm  ' + outfile)

    with open(outfile, 'w') as f:
        f.write('\n'.join(output)+'\n')
