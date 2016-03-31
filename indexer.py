import subprocess
import os
import sys


def index():
    filename = 'directories.txt'
    paths = []
    with open(filename, 'r') as f:
        r = f.readlines()
        paths = [str.strip(p) for p in r]

    logfile = open('python-indexer.log', 'w')

    for path in paths:
        args = [
            '/usr/local/polar/nutch/runtime/local/bin/nutch',
            'index',
            '-Dsolr.server.url=http://polar.usc.edu/solr/polar2'
        ]

        crawldb = os.path.join(path, 'crawldb')
        if os.path.isdir(crawldb):
            args.append('-crawldb')
            args.append(crawldb)

        linkdb = os.path.join(path, 'linkdb')
        if os.path.isdir(linkdb):
            args.append('-linkdb')
            args.append(linkdb)

        args.extend([
            '-segmentDir',
            os.path.join(path, 'segments'),
            '-normalize',
            '-filter'
        ])

        code = subprocess.call(args, stderr=subprocess.STDOUT, stdout=logfile)
        if code == -1:
            sys.stderr.write('Error occured for path {}. Check log file for details.'.format(path))
        else:
            sys.stdout.write('Indexed {} successfully.'.format(path))

if __name__ == "__main__":
    index()
