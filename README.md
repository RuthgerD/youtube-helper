# youtube-dl-helper

stuff you need for bare minimum:
* youtubedl installed (and in PATH for windows)
what you also want to use extract.py:
* kid3-cli installed (and in PATH for windows)

synchronize.py:
utilizes youtube-dl to download music listed in songs.txt from the web


options: 

--download: (enabled by default)
downloads songs from songs.txt without checking if the file already exists

--download-album
downloads songs from songs.txt with checking if the file already exists, handy for keeping a large music library

--update
generates a songs.txt from your music library

songs.txt:
folder indicators:
    ~~ means current folder
    ~~/home/user/somedirectory means direct path
    ~#somefolder means relative path from where the script got called

see songs.txt for examples

extract.py:
tries to extract title and artist data from the file name and applying it to the songs' metadata using kid3-cli


options:

--download-thumbnail: (disabled by default)
downloads and applies the thumbnail from youtube to the songs' metadata

