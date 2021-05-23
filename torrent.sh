#!/bin/bash

INPUT=$1
INPUT_DIRS="${INPUT%/tt*}"


find $INPUT_DIRS -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | while read directory; do
  FETCH_DIR="$INPUT_DIRS$directory";
  find $FETCH_DIR -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | while read line; do
    CURRENT_DIR="$FETCH_DIR/$line"
    find $CURRENT_DIR -maxdepth 1 -mindepth 1 -type f -printf '%f\n' | while read file; do
      CURRENT_TORRENT="$CURRENT_DIR/$file"
      OUTPUT_TORRENT="$CURRENT_DIR/output/"
      echo "DOWNLOADING $CURRENT_TORRENT"

      [[ ! -d $OUTPUT_TORRENT ]] && mkdir -v $OUTPUT_TORRENT
      killfile=$(mktemp);
      transmission-cli $CURRENT_TORRENT --download-dir $OUTPUT_TORRENT -f $killfile -ep -u 64 -p $(python -c 'import random; print(random.randint(1024,65535))') "$i" &
      echo 'kill '$(jobs -p | tail -1)'; rm -f "$0"' > "$killfile";
      chmod +x "$killfile"
    done
  done
done

