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

def makepdf(jpegdir,outpath):
    jpeglist = []
    for filename in sorted(os.listdir(jpegdir)):
        if os.path.splitext(filename)[1] == '.jpg':
            jpeglist.append(os.path.join(jpegdir,filename))
    subprocess.check_call(shlex.split("convert -compress jpeg -format pdf {jpegfiles} {outpath}".format(jpegfiles=' '.join(jpeglist), outpath=outpath)))

def makecbz(jpegdir,outpath):
    cbzfile = zipfile.ZipFile(outpath,'w')
    for filename in sorted(os.listdir(jpegdir)):
        if os.path.splitext(filename)[1] == '.jpg':
            cbzfile.write(os.path.join(jpegdir,filename))
    cbzfile.close()
    
def main():
    if len(sys.argv) != 3:
        sys.exit('Usage: %s SOURCEDIR OUTFILE' % sys.argv[0])
    tempdir = tempfile.mkdtemp()
    print tempdir
    sourcedir = sys.argv[1]
    for i in os.listdir(sourcedir):
        if os.path.splitext(i)[1] == '.cng':
            print os.path.join(sourcedir,i)
            decodepage(os.path.join(sourcedir,i),os.path.join(tempdir,os.path.splitext(i)[0]+'.jpg'))
    if os.path.splitext(sys.argv[2])[1] == '.pdf':
        makepdf(tempdir,sys.argv[2])
    elif os.path.splitext(sys.argv[2])[1] == '.cbz':
        makecbz(tempdir,sys.argv[2])
    shutil.rmtree(tempdir)
    
    
if __name__ == "__main__":
    main()