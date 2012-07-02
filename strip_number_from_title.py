#!/usr/bin/env python
import sys, os, eyeD3, glob, re, shutil

pretend = 0
copy = 0
directory = ''
for arg in sys.argv[1:]:
    if arg == '-p':
        pretend = 1
    elif arg == '-c':
        copy = 1
    elif arg[0] == '-' or arg == '-h':
        print 'Usage: '+sys.argv[0]+' [-h] [-p] [-c] [mp3 directory]'
        print 'Pretend mode: -p'
        print 'Copy only: -c'
        print 'Help: -h'
        sys.exit(1)
    else:
        directory = arg
tag = eyeD3.Tag()

# Move a single ORF.
def update_file(file):
    try:
        tag.link(file)
        title = format(tag.getTitle())
        match = re.search(r"(\d\d\.)\.?\W+(\w.+)", title)
        if (match):
            track_number = match.group(1)
            track_title = match.group(2)
            tag.setTitle(track_title)
            tag.setTrackNum(track_number)
            tag.update()
            print "%s" % track_title
        #else:
            #print "No match found in %s" % title

    except ValueError,v:
        print 'ValueError %s' % v

def update_files(dir):
    for file in glob.glob(dir + '/*mp3'):
        update_file(file)


def dirRead(dir):
    update_files(dir)
    for i in os.listdir(dir):
        path = os.path.join(dir, i)
        if os.path.isdir(path):
            dirRead(path)

def main():
    dirRead(directory)

if __name__ == '__main__':
    main()
