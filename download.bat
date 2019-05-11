@echo off
for /F "usebackq tokens=*" %%A in ("songs.txt") do (
  echo ---- Downloading song: %%A ----
  youtube-dl.exe --rm-cache-dir
  youtube-dl.exe "%%A" --extract-audio --audio-format mp3 --add-metadata --audio-quality 4 --embed-thumbnail -o "%(title)s.%(ext)s"
)
