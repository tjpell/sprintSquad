import glob
import json
import os
import sys

def process_lines(json_lines, outlist):
    """
    when given JSON, this should proccess the json_lines and append the result to the outlist

    :param json_lines: JSON formatted input
    :param outlist: lines of "name    age" formatted strings
    :return: None, modifies global variables
    """

    # we should split out the conditionals to create each line one at a time so that our output is correct
    key_lines = [l for l in json_lines if 'name' in l and 'prop' in l and 'age' in l['prop']]  # keys exist
    lines = [l for l in key_lines if l.get('name') and l.get('prop').get('age')]  # keys aren't null
    names = [l['name'] for l in lines]
    ages = [l['prop']['age'] for l in lines]
    for n, a in zip(names, ages):
        outlist.append(n + '\t' + str(a))

def write_JSON_if_valid(json_blob, outpath):
    """
    when given a JSON, determines whether the blob is of the appropriate format
    given in the instructions. If so, the name and age are appended to the output file.

    input: JSON blob
    output: path of outfile
    """
    if not os.path.exists(os.path.dirname(outpath)):
        os.makedir(os.path.dirname(outpath))
    if 'name' in json_blob and 'prop' in json_blob and 'age' in json_blob['prop']:
        with open(outpath, 'a') as of:
            of.write(json_blob['name'] + '\t' + str(json_blob['prop']['age']))


def extract_Data(infile, outlist):
    """
    infile: file of JSON blobs to be processed
    outlist: list of strings containing names and ages extracted from properly formatted JSON blobs
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

        process_lines(json_lines, outlist)


def main():
    prefix = sys.argv[1]  # get prefix from deploy.py
    os.system('cd ../..')  # move down so that we can access srv directory
    os.system('pwd')
    path = '/srv/runme/' + prefix + '/'  # path that we are writing to

    file = path + 'Raw.txt'
    output = []

    try:
        extract_Data(file, output)
    except ValueError:
        print "oops."

    outfile = path + 'proc.txt'
    os.system('rm  ' + outfile)

    with open(outfile, 'w') as f:
        f.write('\n'.join(output)+'\n')


if __name__ == "__main__":
    main()