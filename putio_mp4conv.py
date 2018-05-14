#!/usr/bin/python

import putio
from subprocess import call
import os

dl_dirname = 'youtube'
ul_dirname = 'ytmp3'
done_dirname = 'ytconverted'

#solve this by search api request and full text match
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


def convert_and_upload_every_file(fileList=[]):
    ulid = get_file_id(ul_dirname)
    for id in fileList:
        filename = download_video(id)
        print("file: " + filename)
        mp3_filepath = convert_to_mp3(filename)
        upload_mp3(mp3_filepath,ulid)
        cleanup(id, mp3_filepath)
        

def download_video(id):
    return putio.download_file(confdict, id, "./working")


def convert_to_mp3(filename_with_extension):
    indir = "./working"
    outdir = "./outdir"

    if filename_with_extension[-4:] == ".mp4":
        return convert_mp4_to_mp3(filename_with_extension, indir, outdir)
    elif filename_with_extension[-5:] == ".webm": 
        return convert_webm_to_mp3(filename_with_extension,indir,outdir)


def convert(convertfunc):

    def convert_wrapper(filename_with_extension  ,indir, outdir):
        filename = ".".join(filename_with_extension.split(".")[0:-1])

        if not os.path.exists(outdir):   
            os.makedirs(outdir)

        convertfunc(filename, indir, outdir)    
        os.remove(indir + "/" + filename_with_extension)
        return outdir + "/" + filename + ".mp3"

    return convert_wrapper


@convert
def convert_mp4_to_mp3(filename, indir, outdir):
    call(["ffmpeg", "-i", indir + "/" + filename + ".mp4",  "-b:a", "192K", 
            "-vn", outdir + "/" + filename + ".mp3"])


@convert
def convert_webm_to_mp3(filename, indir, outdir):
    call(["ffmpeg", "-i", indir + "/" + filename + ".webm", "-vn", "-ab", 
            "128k", "-ar", "44100", "-y", outdir + "/" + filename + ".mp3"])


def upload_mp3(mp3_path, upload_id):
    putio.upload_file(confdict, mp3_path, upload_id)


def cleanup(id, mp3_path):
    move_video_in_putio(id)
    delete_mp3_on_host(mp3_path)


def move_video_in_putio(id):
    done_id = get_file_id(done_dirname)
    putio.move_file(confdict, id, done_id)


def delete_mp3_on_host(mp3_path):
    os.remove(mp3_path)


def main():
    global confdict 
    confdict = putio.config()
    fileList = get_file_list()
    convert_and_upload_every_file(fileList)


if __name__ == '__main__':
    main()
