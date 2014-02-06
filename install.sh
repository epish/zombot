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

if [ $# -eq 2 ]; then
	USER="$1"
	PASSWD="$2"
else
	echo "found $# args Usage `basename $0` username password"
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
	ln -s $(pwd)/$PRGDIR/run.sh "$USERDIR"/
	exec sed -e "s/#EMAIL#/$USER/g" -e "s/#PASSWD#/$PASSWD/g" $PRGDIR/settings.example.ini > "$USERDIR/settings.ini"
	echo "Directory populated"
else
	exit $?
fi
