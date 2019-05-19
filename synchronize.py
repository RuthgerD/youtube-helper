import urllib.request
import re
import os
import glob
import subprocess
import sys
import platform
from extract import cleanTitle


def download(URL, destination = os.getcwd(), title = "%(title)s"):
    if platform.system() == "Windows":
        youtubedl = "youtube-dl.exe"
    elif platform.system() == "Linux":
        youtubedl = "youtube-dl"
    destination = os.path.join(destination, title + ".%(ext)s")

    # Noteworthy: defaults to youtubesearch, spits out mp3 with audio quality 4 and embeds thumbnail
    command = youtubedl + " \"" + URL + "\" --default-search \"ytsearch\" --rm-cache-dir --extract-audio --audio-format mp3 --add-metadata --audio-quality 4 --embed-thumbnail -o \""+ destination +"\""
    print("\n-----")
    subprocess.run(command,  shell=True)
    print("-----\n")

def getData(URL):
    if platform.system() == "Windows":
        youtubedl = "youtube-dl.exe"
    elif platform.system() == "Linux":
        youtubedl = "youtube-dl"
    # Get title and id without downloading anything
    command = youtubedl + " \"" + URL + "\" --skip-download --get-title --get-id"
    rawdata = subprocess.check_output(command,  shell=True)
    # Replace \n with ~~~ to not mess with the regex
    rawdata = re.search("(?<=\').*(?=\')", str(rawdata).replace("\\n", "~~~")).group()
    # Splot title and id
    data = []
    data.append(re.search("^.*?(?=~~~)", rawdata).group())
    data.append("https://www.youtube.com/watch?v="+re.search("(?<=~~~).*?(?=~~~$)", rawdata).group())
    return data

def reconstruct(file, workdir, ADownload):
    # Check if we have song.txt
    if not os.path.isfile(os.path.join(workdir, file)):
        input("song.txt not found,\nPress enter to close")
        return
    if not ADownload:
        print(platform.system() + " | Direct Download Mode")
    else:
        print(platform.system() + " | Album Download Mode")

    # Extract all individual lines from song.txt
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
                    os.chdir(line.replace("~~", ""))
                else:
                    os.chdir(line.replace("~~", ""))

            if line == "~~":
                print("\nOutput Folder: " + os.getcwd())
            else:
                print("\nOutput Folder: " + line.replace("~~", ""))

            files = []
            for name in glob.glob('*.mp3'):
                files.append(name.replace(".mp3", ""))
        else:
            command = ""
            link = ""
            title = ""
            # --download-album will check if the file is already there so playlists are illegal :)
            if re.search("(youtube.com|youtu.be)", line):
                line = re.sub("&f.*", "", line)
                line = re.sub("\?t=.*", "", line)
                id = re.search("((?<=watch\?v\=)|(?<=youtu\.be\/)).*", line).group()
                command = line
                data = getData(id)
                title = data[0]
                link = data[1]
            elif re.search("(ytsearch:|scsearch:)", line):
                command = line
                data = getData(line)
                title = data[0]
                link = data[1]
                if re.search("scsearch:", command):
                    link = link.replace("https://www.youtube.com/watch?v=", "https://w.soundcloud.com/player/?url=https://api.soundcloud.com/tracks/")
            else:
                command = line
                data = getData("ytsearch:" + line)
                title = data[0]
                link = data[1]
            title = title.replace("/", "_").replace("\\", "_")
            print("  Command: " + command)
            print("  Title: " + title)
            print("  Direct: " + link)
            local = False
            for file in files:
                test = cleanTitle(title)
                file = cleanTitle(file)
                test = str(re.sub("([- [\]{}()*+?.,\\^$|#\s])", "",test))
                file = str(re.sub("([- [\]{}()*+?.,\\^$|#\s])", "",file))
                if re.search(test, file, re.IGNORECASE) and ADownload:
                    local = True
            if local:
                print("  Song Already Local.")
            else:
                print("  Downloading..")
                download(command, os.getcwd(), title)


        print()

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


def main():
    directory = os.getcwd()

    mode = ""
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
    if len(sys.argv) == 3:
        directory = sys.argv[2]
        os.chdir(directory)




    if mode == "--download":
        reconstruct('songs.txt', directory, False)

    elif mode == "--update":
        construct(directory)

    elif mode == "--download-album":
        reconstruct('songs.txt', directory, True)
    else:
        return

if __name__== "__main__":
    main()
