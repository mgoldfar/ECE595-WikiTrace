#! /bin/bash 

# get NUMHOSTS live hosts
for h in $(get_live_ecelinux_hosts.sh)
do
		echo "Killing grinder processed on $h"
		CMDSTR="killall grinder;"
		ssh -o StrictHostKeyChecking=no mgoldfar@$h "$CMDSTR"
done

exit 0