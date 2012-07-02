# Hello, this script is written in Python - http://www.python.org
# doublesdetector.py 1.0p
import os, os.path, string, sys, sha

message = """
doublesdetector.py 1.0p

This script will search for files that are identical
(whatever their name/date/time).

  Syntax : python %s <directories>

      where <directories> is a directory or a list of directories
      separated by a semicolon (;)

Examples : python %s c:\windows
           python %s c:\;d:\;e:\ > doubles.txt
           python %s c:\program files > doubles.txt

This script is public domain. Feel free to reuse and tweak it.
The author of this script Sebastien SAUVAGE <sebsauvage at sebsauvage dot net>
http://sebsauvage.net/python/
""" % ((sys.argv[0], )*4)

def fileSHA ( filepath ) :
    """ Compute SHA (Secure Hash Algorythm) of a file.
        Input : filepath : full path and name of file (eg. 'c:\windows\emm386.exe')
        Output : string : contains the hexadecimal representation of the SHA of the file.
                          returns '0' if file could not be read (file not found, no read rights...)
    """
    try:
        file = open(filepath,'rb')
        digest = sha.new()
        data = file.read(65536)
        while len(data) != 0:
            digest.update(data)
            data = file.read(65536)
        file.close()
    except:
        return '0'
    else:
        return digest.hexdigest()

def detectDoubles( directories ):
    fileslist = {}
    # Group all files by size (in the fileslist dictionnary)
    for directory in directories.split(';'):
        directory = os.path.abspath(directory)
        sys.stderr.write('Scanning directory '+directory+'...')
        os.path.walk(directory,callback,fileslist)
        sys.stderr.write('\n')

    sys.stderr.write('Comparing files...')
    # Remove keys (filesize) in the dictionnary which have only 1 file
    for (filesize,listoffiles) in fileslist.items():
        if len(listoffiles) == 1:
            del fileslist[filesize]

    # Now compute SHA of files that have the same size,
    # and group files by SHA (in the filessha dictionnary)
    filessha = {}
    while len(fileslist)>0:
        (filesize,listoffiles) = fileslist.popitem()
        for filepath in listoffiles:
            sys.stderr.write('.')
            sha = fileSHA(filepath)
            if filessha.has_key(sha):
                filessha[sha].append(filepath)
            else:
                filessha[sha] = [filepath]
    if filessha.has_key('0'):
        del filessha['0']

    # Remove keys (sha) in the dictionnary which have only 1 file
    for (sha,listoffiles) in filessha.items():
        if len(listoffiles) == 1:
            del filessha[sha]
    sys.stderr.write('\n')
    return filessha

def callback(fileslist,directory,files):
    sys.stderr.write('.')
    for fileName in files:
        filepath = os.path.join(directory,fileName)
        if os.path.isfile(filepath):
            filesize = os.stat(filepath)[6]
            if fileslist.has_key(filesize):
                fileslist[filesize].append(filepath)
            else:
                fileslist[filesize] = [filepath]

if len(sys.argv)>1 :
    doubles = detectDoubles(" ".join(sys.argv[1:]))
    print 'The following files are identical:'
    print '\n'.join(["----\n%s" % '\n'.join(doubles[filesha]) for filesha in doubles.keys()])
    print '----'
else:
    print message
