import urllib.request
import re
import os
import glob
import subprocess
import sys
import platform

def download(URL, destination = os.getcwd()):
    destination = os.path.join(destination, "%(title)s.%(ext)s")

    if platform.system() == "Windows":
        youtubedl = "youtube-dl.exe"
    elif platform.system() == "Linux":
        youtubedl = "youtube-dl"
    command = youtubedl + " \"" + URL + "\" --rm-cache-dir --extract-audio --audio-format mp3 --add-metadata --audio-quality 4 --embed-thumbnail -o \""+ destination +"\""
    subprocess.run(command,  shell=True)
    print("  Finished")

def getTitle(URL):
    command = "youtube-dl \"" + URL + "\" --quiet --skip-download --get-title"
    title = subprocess.check_output(command,  shell=True)
    title = re.search("(?<=\').*(?=\')", str(title).replace("\\n", "")).group()
    return title

def reconstruct(file, workdir):
    print(platform.system() + " | Download Mode")

    with open(os.path.join(workdir, file), 'r') as f:
        content = [line.strip() for line in f]

    files = []
    for line in content:
        album = ""
        song = ""
        if re.match("~#.*", line):
            print("\nOutput Folder: " + line.replace("~#", ""))
            album = line.replace("~#", "")
            albumdir = os.path.join(workdir, album)

            if not os.path.exists(albumdir):
                os.mkdir(albumdir)

            os.chdir(albumdir)
            files = []
            for name in glob.glob('*.mp3'):
                files.append(name.replace(".mp3", ""))
        elif re.match("~~.*", line):
            if line == "~~":
                os.chdir(workdir)
            else:
                if not os.path.exists(line.replace("~~", "")):
                    os.makedirs(line.replace("~~", ""))
                    print("New Directory Created")
                else:
                    os.chdir(line.replace("~~", ""))


            print("\nOutput Folder: " + line.replace("~~", ""))

            files = []
            for name in glob.glob('*.mp3'):
                files.append(name.replace(".mp3", ""))
        else:
            song = line
            if re.search("(youtube.com|youtu.be)", line):
                print("  ID: " + re.search("((?<=watch\?v\=)|(?<=youtu\.be\/)).*", line).group() + "\n  Grabbing title..")
                song = getTitle(line)
            print("  " + song)
            local = False
            for file in files:
                test = str(re.sub("([-[\]{}()*+?.,\\^$|#\s])", r"\\\1",song))
                if re.search(test, file, re.IGNORECASE):
                    local = True
            if local:
                print("  Song Already Local.")
            else:
                print("  Song Not Found, Downloading.")
                if re.search("(youtube.com|youtu.be)", line):
                    download(line, os.getcwd())
                else:
                    download("ytsearch:" + song, os.getcwd())

def construct(workdir):
    print("Update Mode")
    albums = [""] + next(os.walk('.'))[1]
    output = []
    for album in albums:
        #if re.search("^#.*", album) or album == "":
        os.chdir(os.path.join(workdir, album))
        music = False
        for name in glob.glob('*.mp3'):
            music = True
        if music:
            if album == "":
                output.append("~~\n")
                print("~~")
            else:
                output.append("~#" + album + "\n")
                print(album)

            for name in glob.glob('*.mp3'):
                print("  "+name.replace(".mp3", ""))
                output.append(name.replace(".mp3", "") + "\n")
    os.chdir(workdir)
    outF = open("songs.txt", "w")
    outF.writelines(output)
    outF.close()

directory = os.getcwd()

mode = "download"
if len(sys.argv) >= 2:
    if sys.argv[1] == "update":
        mode = sys.argv[1]
if len(sys.argv) == 3:
    directory = sys.argv[2]
    os.chdir(directory)


if mode == "download":
    reconstruct('songs.txt', directory)

elif mode == "update":
    construct(directory)
