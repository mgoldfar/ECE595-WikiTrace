#! /bin/bash

NHOSTS=0
if (( $# == 1 ))
then
	NHOSTS=$1
fi

(( i=0 ))
for h in 0{1..9} 1{0..9} 2{0..9}
do
		host=ecelinux${h}.ecn.purdue.edu		
		if ping -c1 -t1 $host >/dev/null 2>/dev/null
		then
				echo $host
				((i++))
		fi
		
		if (( NHOSTS > 0 && i > NHOSTS ))
		then
			break
		fi
done

if (( NHOSTS > 0 && i < NHOSTS - 1 ))
then

	LIVE=$((i+1))
	echo "error: Only found $LIVE of $NHOSTS alive!"
	exit 1
fi

exit 0