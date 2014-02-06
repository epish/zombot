#!/bin/sh


# resolve links - $0 may be a softlink
PRG="$0"

while [ -h "$PRG" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done

PRGDIR=`dirname "$PRG"`

EXECUTABLE=src/main.py
PYTHONPATH="$PRGDIR"/lib
LC_CTYPE=en_GB.UTF-8

echo "PRGDIR $PRGDIR"
export PYTHONPATH="$PRGDIR"/lib
python "$PRGDIR"/"$EXECUTABLE" -c
