#! /bin/bash

for h in 0{1..9} 1{0..9} 2{0..9}
do
		host=ecelinux${h}.ecn.purdue.edu		
		if ping -c1 -t1 $host >/dev/null
		then
				echo $host
		fi
done

exit 0