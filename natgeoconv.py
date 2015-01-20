#!/usr/bin/env python

import os
import subprocess
import tempfile
import shutil
import shlex
import sys
import zipfile

def decodepage(inputpath,outputpath):
    jpeg = bytearray(open(inputpath,'rb').read())
    for byte in range(len(jpeg)):
        jpeg[byte] ^= 0xEF
    open(outputpath,'wb').write(jpeg)

def makecbz(jpegdir,outpath):
    cbzfile = zipfile.ZipFile(outpath,'w')
    for filename in sorted(os.listdir(jpegdir)):
        if os.path.splitext(filename)[1] == '.jpg':
            cbzfile.write(os.path.join(jpegdir,filename))
    cbzfile.close()
    
def processdir(dirname, names):
    """Returns path to decoded jpegs or None if nothing decoded"""
    decodedfiles = False
    tempdir = tempfile.mkdtemp()
    for filename in names:
        if os.path.splitext(filename)[1] == '.cng':
            decodepage(os.path.join(dirname,filename),os.path.join(tempdir,os.path.splitext(filename)[0]+".jpg"))
            decodedfiles = True
    return tempdir if decodedfiles else None
        
def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: %s SOURCEDIR OUTDIR' % sys.argv[0])
    sourcedir = sys.argv[1]
    for (dirpath, dirnames, filenames) in os.walk(sourcedir):
        jpegdir = processdir(dirpath,filenames)
        if jpegdir != None: makecbz(jpegdir,os.path.join(sys.argv[2],os.path.split(dirpath)[-1]+'.cbz'))
    
if __name__ == "__main__":
    main()