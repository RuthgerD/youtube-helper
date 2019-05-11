while read -r p; do
  echo "---- Downloading song: $p ----"
  youtube-dl --rm-cache-dir
  youtube-dl $p --extract-audio --audio-format mp3 --add-metadata --audio-quality 5 -o "%(title)s.%(ext)s.%(ext)s"
done <songs


