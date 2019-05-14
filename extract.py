import re
import glob
import os
import subprocess
import sys

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

retardwords = ["\[.*\] -", "Dubstep- ", "-- Lyrics [CC]", ", Inc", " - Diversity Release"]
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

    for word in retardwords:
        if re.match(word, song):
            song = song.replace(re.search(word, song).group(), "")

    song = song.replace("–", "-")
    song = song.replace("【", "(")
    song = song.replace("】", ")")
    song = song.replace("[", "(")
    song = song.replace("]", ")")

    #try:
    for i in range(song.count('(')):
        delete = re.search("\(.*?\)", song).group()
        song = song.replace(delete, "")
    if " ft. " in song or " Ft. " in song or " FT. " in song or " fT. " in song:
        delete = re.search("(?i) ft\. .*?((?= -)|$)", song).group()
        song = song.replace(delete, "")
    #except:
        #print("somthing went wrong >w<")

    song = song.strip(' ')
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
                #artists.append("NIGGGAAAA")
                #input("AAAAAAAAAAAAAAAAAAAAAAA")
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

    command = "kid3-cli -c \"select '" + files[songcount].replace("'", "\\'") + "'\" -c \"set title '" + title.replace("'", "\\'") + "'\"" + artistcommand + " -c \"set 'track number' '" + str(songcount) + "'\""
    print(command)
    subprocess.run(command,  shell=True)

    songcount += 1
