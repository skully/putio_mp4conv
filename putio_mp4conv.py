#!/usr/bin/python

import putio

dl_dirname = 'youtube'
ul_dirname = 'ytmp3'

def get_file_id(name):
    #it's in the root!
    root = putio.get_filelist(confdict, 0)
    rootfiles = [e["id"] for e in root["files"] if e["name"]==name]
    if len(rootfiles) == 1:  
        return rootfiles[0]
    else:
        return 0

def get_file_list():
    dlid = get_file_id(dl_dirname)
    dlfilelist = putio.get_filelist(confdict,dlid)
    dlfileids = [fid["id"] for fid in dlfilelist["files"]]
    return dlfileids


def convert_every_file(fileList=[]):
    #ulid = get_file_id(ul_dirname)
    for i in fileList:
        download_mp4()
        convert_mp4_to_mp3()
        upload_mp3()
        cleanup()

def download_mp4():
    pass

def convert_mp4_to_mp3():
    pass

def upload_mp3():
    pass

def cleanup():
    pass

def main():
    global confdict 
    confdict = putio.config()
    fileList = get_file_list()
    convert_every_file(fileList)



if __name__ == '__main__':
    main()
