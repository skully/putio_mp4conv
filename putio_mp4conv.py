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
        filename = download_mp4(id)
        print("file: "+filename)
        mp3_filepath = convert_mp4_to_mp3(filename)
        upload_mp3(mp3_filepath,ulid)
        cleanup(id, mp3_filepath)
        

def download_mp4(id):
    return putio.download_file(confdict, id, "./working")


def convert_mp4_to_mp3(filename_with_extension):
    indir = "./working"
    outdir = "./outdir"
    print(filename_with_extension[0:-4]) 
    if filename_with_extension[-4:] == ".mp4":
        filename = filename_with_extension[0:-4]
        print("-- converting {0}/{2}.mp4 to {1}/{2}.mp3 --".format(indir, outdir, filename))
        call(["mplayer", "-novideo", "-nocorrect-pts", "-ao", "pcm:waveheader", indir + "/" + filename +".mp4"])

        if not os.path.exists(outdir):   
            os.makedirs(outdir)

        call(["lame", "-v", "audiodump.wav", outdir + "/" + filename + ".mp3"])
        os.remove("audiodump.wav")
        os.remove(indir + "/" + filename_with_extension)
        print(outdir + "/" + filename + ".mp3"+"mp4")
        return outdir + "/" + filename + ".mp3"

    elif filename_with_extension[-5:] == ".webm": 
        filename = filename_with_extension[0:-5]
        call(["ffmpeg", "-i", indir + "/" + filename_with_extension, "-vn", "-ab", "128k", "-ar", "44100",
                "-y", outdir + "/" + filename + ".mp3"])
        #os.remove(indir + "/" + filename_with_extension)
        print(outdir + "/" + filename + ".mp3"+"webm")
        return outdir + "/" + filename + ".mp3"



def upload_mp3(mp3_path, upload_id):
    putio.upload_file(confdict, mp3_path, upload_id)


def cleanup(id, mp3_path):
    move_mp4_in_putio(id)
    delete_mp3_on_host(mp3_path)


def move_mp4_in_putio(id):
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
