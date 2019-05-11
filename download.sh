while read -r p; do
  echo "---- Downloading song: $p ----"
  youtube-dl --rm-cache-dir
  youtube-dl "$p" --extract-audio --audio-format mp3 --add-metadata --audio-quality 4 --embed-thumbnail -o "%(title)s.%(ext)s"
done <songs.txt


