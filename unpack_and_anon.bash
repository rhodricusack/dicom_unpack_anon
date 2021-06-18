#!/bin/bash

DATAPATH=~/mridata
ARCHIVE=$1
ARCHIVE_NOEXT=${ARCHIVE%.zip}
ARCHIVE_NAME=${ARCHIVE_NOEXT##*/}

echo "Unzipping $ARCHIVE_NAME"
mkdir -p $DATAPATH/$ARCHIVE_NAME
# unzip -d $DATAPATH/$ARCHIVE_NAME -o $1

# Make sure all files are anonymised
echo $DATAPATH/$ARCHIVE_NAME


for f in $(find $DATAPATH/$ARCHIVE_NAME -name '*.dcm' -type f); do
  echo $f
#  dcmodify -exec dcmodify -ie -nb -ea "(0010,0010)" -ea "(0010,0030)" $f \;
    dcmdump +L +P "0010,0020" $f | cut -d "[" -f2 | cut -d "]" -f1
done


