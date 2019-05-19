import urllib.request
import re
import os
import glob
import subprocess
import sys
import platform

def downloadThumb(song):
    if platform.system() == "Windows":
        kid3 = "kid3-cli.exe"
        youtubedl = "youtube-dl.exe"
    elif platform.system() == "Linux":
        kid3 = "kid3-cli"
        youtubedl = "youtube-dl"


def cleanTitle(title):
    retardwords = ["\[.*\] -", "Dubstep- ", "-- Lyrics [CC]", ", Inc", " - Diversity Release"]

    for word in retardwords:
        if re.match(word, title):
            title = title.replace(re.search(word, title).group(), "")

    title = title.replace("–", "-")
    title = title.replace("【", "(")
    title = title.replace("】", ")")
    title = title.replace("[", "(")
    title = title.replace("]", ")")


    title = re.sub("ft.", "ft.", title, re.IGNORECASE)
    title = re.sub("feat.", "ft.", title, re.IGNORECASE)


    for i in range(title.count('(')):
        delete = re.search("\(.*?\)", title).group()
        title = title.replace(delete, "")

    if " ft. " in title:
        delete = re.search(" ft\. .*?((?= -)|$)", title, re.IGNORECASE).group()
        title = title.replace(delete, "")
    title = title.replace(".", " ")
    title = title.replace("  ", " ")
    title = title.strip(' ')
    return title

def main():
    directory = os.getcwd()
    print(len(sys.argv))
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            directory = sys.argv[1]
    else:
        print("No directory given using current one")

    os.chdir(directory)
    files = []
    songs = []
    print(os.getcwd())
    for name in glob.glob('*.mp3'):
        files.append(os.path.abspath(name))
        songs.append(name.replace(".mp3", ""))
    print(songs)

    defaultsingle = [" & ", ", ", " ft. "]
    defaultdual = [", ", " ft. "]
    commadual = [" & ", " ft. "]
    defaulttrio = [" ft. "]

    songcount = 0
    for song in songs:
        print("\n----------\n"+song)
        state = 0
        title = ""
        artists = []

        song = cleanTitle(song)
        downloadThumb(song)
        print("CLEANED: " + song)
        if " - " in song:
            before = re.search(".*-", song).group()
            #after = re.search("(?<=-)".*", song).group()
            if not any(x in before for x in defaultsingle):
                state = 1
            elif not any(x in before for x in defaultdual):
                    state = 2
            elif not any(x in before for x in commadual):
                    state = 3
            elif not any(x in before for x in defaulttrio):
                    state = 4
            if state == 1:
                    title = re.search("(?<= - ).*", song).group()
                    artists.append(re.search(".*(?= - )", song).group())
                    title = re.search("(?<= - ).*", song).group()
                    title_search = re.findall("(?:(?<= x )|^)(.*?)(?:(?= x )|(?= - ))", before, re.IGNORECASE)
                    print(title_search)
            if state == 2:
                title = re.search("(?<= - ).*", song).group()
                artists.append(re.search(".*(?= & )", song).group())
                artists.append(re.search("(?<= & ).*(?= - )", song).group())
            if state == 3:
                title = re.search("(?<= - ).*", song).group()
                artists.append(re.search(".*(?=, )", song).group())
                artists.append(re.search("(?<=, ).*(?= - )", song).group())
            if state == 4:
                title = re.search("(?<= - ).*", song).group()
                artists.append(re.search(".*(?=, )", song).group())
                artists.append(re.search("(?<=, ).*(?= & )", song).group())
                artists.append(re.search("(?<= & ).*(?= - )", song).group())
        else:
                title = song
                artists.append("Nobody")
        if "Remix" in files[songcount] or "remix" in files[songcount] or "REMIX" in files[songcount]:
            title += " (Remix)"
        print ("\ntitle: " + title + "\n"+ "artist: " + str(artists) + "\n")
        print(files[songcount])

        artistcommand = ""
        j = 0
        for artist in artists:
            artistcommand += " -c \"set artist["+str(j)+"] '" + artists[j].replace("'", "\\'") + "'\""
            j += 1
        if platform.system() == "Windows":
            kid3 = "kid3-cli.exe"
        elif platform.system() == "Linux":
            kid3 = "kid3-cli"
        command = kid3 + " -c \"select '" + files[songcount].replace("'", "\\'") + "'\" -c \"set title '" + title.replace("'", "\\'") + "'\"" + artistcommand + " -c \"set 'track number' '" + str(songcount) + "'\""
        print(command)
        subprocess.run(command,  shell=True)

        songcount += 1
if __name__== "__main__":
    main()
