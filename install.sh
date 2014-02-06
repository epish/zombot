#!/bin/sh

E_BADARGS=85
E_BADDIR=85

check_dir()
{
	if [ -d "$USERDIR" ]
	then
		echo "$USERDIR directory exists. Try another."	
		return $E_BADDIR
	fi
	echo "Dir doesn'r exist"
	return 0
}

if [ -n "$1" ]
then
	USER=$1
else
	echo "Usage `basename $0` username"
	exit $E_BADARGS
fi


PRGDIR=`dirname "$0"`
USERDIR="$PRGDIR/var/$USER"
check_dir

#echo "checkdir: $?"
if [ $? -eq 0 ]
then
	echo "making dir $USERDIR"
	mkdir "$USERDIR"
	echo "making symlik $PRGDIR/run.sh"
	ln -s $(pwd)/run.sh "$USERDIR"/
	cp ./settings.ini "$USERDIR"
	echo "Directory populated"
else
	exit $?
fi
