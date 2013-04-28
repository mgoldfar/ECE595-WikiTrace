#! /bin/bash -e

if (( $# < 4 ))
then
	echo "usage: launch_tests_ecelinux.sh <num_hosts> <test_name> <nruns> <script> [addl files]"
	echo "  <num_hosts>   The number of ecelinux hosts to run on."
	echo "  <test_name>   Name to identify the test (will be used as the prefix of the request)"
	echo "  <nruns>       Number of run to execute the test for"
	echo "  <script>      The main grinder script to run"
	echo "  [addl files]  Additional files required by the script (e.g. modules, input files etc.)"
	echo 
	exit 1
fi

NUMHOSTS=$1
TESTNAME=$2
NRUNS=$3
shift 3

# get NUMHOSTS live hosts
hosts=($(get_live_ecelinux_hosts.sh $NUMHOSTS))

((baseid=0))
for h in ${hosts[*]}
do
		CMDINITSTR="source ~/.bash_profile; cd wiki_trace/grinderscripts; cat ./run_test.sh"
		CMDSTR="./run_test.sh $TESTNAME $baseid $NRUNS $@"
		ssh -o StrictHostKeyChecking=no mgoldfar@$h "$CMDINITSTR $CMDSTR" &
		((baseid++))
done &

# wait for all remote hosts to exit
wait $!

exit 0