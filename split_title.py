#!/usr/bin/env python
import sys, os, eyeD3, glob, shutil

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
        print "%s is correctly located already." % newfile
    else:
        shutil.move(src,dir)

def get_title(file):
    tag.link(file)
    #title = str(tag.getTitle())
    title = format(tag.getTitle()) #.encode("utf-8")
    return title

def ensure_directory_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def move_files(dir):
    for file in glob.glob(dir + '/*mp3'):
        try:
            title = str(get_title(file))
            print "Look " + str(title.find('-'))
            if title.find('-')>-1: # if it has - parse it out
                number,artist,title = get_title(file).split('-')
                print "artist:" + artist
                print "title:" + title
                tag.link(file)
                tag.setArtist(number,artist)
                tag.setTitle(title)
                tag.update()
            else:
                print "No split found in " + file
            #move_file(file, title)

        except eyeD3.tag.GenreException,(file):
            file = str(file)
            print 'GenreException ' + file

        except:
            print 'Exception ' + file
        #    sys.exit(1)


def dirRead(dir):
    move_files(dir)
    for i in os.listdir(dir):
        path = os.path.join(dir, i)
        if os.path.isdir(path):
            dirRead(path)

def main():
    #reload(sys)
    #sys.setdefaultencoding( "latin-1" )
    dirRead(directory)

if __name__ == '__main__':
    main()
