#!/bin/sh

E_BADDIR=85

if [ $# -eq 1 ]; then
	USER="$1"
else
	echo "found $# args Usage `basename $0` username "
	exit $E_BADARGS
fi

PRGDIR=`dirname "$0"`
cd "$PRGDIR/var/$USER" && ./run.sh
