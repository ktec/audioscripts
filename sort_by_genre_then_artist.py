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
def move_file(src,dst):
    dir, fn = os.path.split(src)
    dir = os.path.join(directory,dst)
    ensure_directory_exists(dir)
    #tag.link(file)
    #artist = str(tag.getArtist())
    newfile = os.path.join(dir,fn)
    if os.path.isfile(newfile):
        sys.stderr.write('.')
        #print "%s is correctly located already." % newfile
    else:
        print "moving %s to %s" % (src,dir)
        shutil.move(src,dir)

def get_genre(tag):
    genre = str(tag.getGenre())
    if genre.find('(')>-1 and genre.find(')')>-1: # if it has () parse it out
        genre = genre.split(')').pop(1)
    return genre

def ensure_directory_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def scan(directory):
    sys.stderr.write('Scanning directory '+directory+'...')
    os.path.walk(directory,callback,None)
    sys.stderr.write('\n')

def callback(fileslist,directory,files):
    for fileName in fnmatch.filter(files, "*.mp3"):
        file = os.path.join(directory,fileName)
        try:
            tag.link(file)
            genre = get_genre(tag)
            artist = tag.getArtist()
            move_file(file, genre+"/"+artist)

        except UnicodeDecodeError, e:
            print "WARNING: Error reading mp3 %s; ignoring illegal characters" % file, e
            continue

        except eyeD3.tag.GenreException,(genreName):
            genreName = str(genreName)
            print 'GenreException ' + genreName

        except:
            print "Sorry problem with file: %s" % file
            print "Unexpected error:", sys.exc_info()[0]
            raise


def main():
    reload(sys)
    sys.setdefaultencoding( "latin-1" )

    scan(directory)


if __name__ == '__main__':
    main()
