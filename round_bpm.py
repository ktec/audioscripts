#!/usr/bin/env python
import sys, os, eyeD3, glob, shutil, fnmatch

pretend = 0
copy = 0
directory = ''
for arg in sys.argv[1:]:
    if arg == '-p':
        pretend = 1
    elif arg == '-c':
        copy = 1
    elif arg == '-g':
        genre = sys.argv[1]
    elif arg[0] == '-' or arg == '-h':
        print 'Usage: '+sys.argv[0]+' [-h] [-p] [-c] [mp3 directory]'
        print 'Pretend mode: -p'
        print 'Copy only: -c'
        print 'Help: -h'
        sys.exit(1)
    else:
        directory = arg
tag = eyeD3.Tag()

def scan(directory):
    sys.stderr.write('Scanning directory '+directory+'...')
    os.path.walk(directory,callback,None)
    sys.stderr.write('\n')

def callback(fileslist,directory,files):
    for fileName in fnmatch.filter(files, "*.mp3"):
        file = os.path.join(directory,fileName)
        try:
            tag.link(file)
            bpm = tag.getBPM()
            #print "Bpm: %s" % bpm
            tag.setBPM(bpm)
            #tag.setGenre(genre)
            tag.update()
            sys.stderr.write('.')

        except UnicodeDecodeError, e:
            print "WARNING: Error reading mp3 %s; ignoring illegal characters" % file, e
            continue

        except:
            print "Sorry problem with file: %s" % file
            print "Unexpected error:", sys.exc_info()[0]
            raise


def main():
    scan(directory)

if __name__ == '__main__':
    main()
